import numpy as np
import tqdm
import subprocess
from comet_ml import Experiment
import time


class Logger:
    def __init__(self, send_logs, tags, parameters):
        self.send_logs = send_logs
        if self.send_logs:
            self.experiment = Experiment(api_key="OZwyhJHyqzPZgHEpDFL1zxhyI",
                                         project_name="drilling-the-hole", workspace="wwydmanski")
        self.sent_mb = 0

        if self.send_logs:
            if tags is not None:
                self.experiment.add_tags(tags)
            if parameters is not None:
                self.experiment.log_parameters(parameters)

    def begin_logging(self, episode_count, steps_per_ep):
        if self.send_logs:
            self.experiment.log_parameter("Episode count", episode_count)
            self.experiment.log_parameter("Max steps per episode", steps_per_ep)

    def log_round(self, actions, reward, cumulative_reward, loss, step):
        if self.send_logs:
            self.experiment.log_metric("Round reward", reward, step=step)
            self.experiment.log_metric("Per-ep reward", cumulative_reward, step=step)
            self.experiment.log_metric("Action 1", actions[0], step=step)
            self.experiment.log_metric("Action 2", actions[1], step=step)

            self.experiment.log_metrics(loss, step=step)

    def log_episode(self, cumulative_reward, state, step):
        if self.send_logs:
            self.experiment.log_metric("Angle", state[0], step=step)
            self.experiment.log_metric("Goal", state[1], step=step)
            self.experiment.log_metric("Cumulative reward", cumulative_reward, step=step)

    def end(self):
        if self.send_logs:
            self.experiment.end()


class Teacher:
    """Class that handles training of RL model in ns-3 simulator

    Attributes:
        agent: agent which will be trained
        env (ns3-gym env): environment used for learning. NS3 program must be run before creating teacher
        num_agents (int): number of agents present at once
    """

    def __init__(self, env, preprocessor=None):
        if preprocessor is not None:
            self.preprocess = preprocessor.preprocess
        else:
            self.preprocess = None

        self.env = env
        self.CW = 16
        self.actions = None  # For debug purposes
        self.debug = None

    # def dry_run(self, agent, steps_per_ep):
    #     obs = self.env.reset()
    #     obs = self.preprocess(np.reshape(obs, (-1, len(self.env.envs), 2)))
    #
    #     with tqdm.trange(steps_per_ep) as t:
    #         for step in t:
    #             self.actions = agent.act()
    #             next_obs, reward, done, info = self.env.step(self.actions)
    #
    #             obs = self.preprocess(np.reshape(next_obs, (-1, len(self.env.envs), 2)))
    #
    #             if (any(done)):
    #                 break

    def train(self, agent, EPISODE_COUNT, max_steps, history_length, send_logs=True, tags=None, parameters=None):
        steps_per_ep = max_steps

        logger = Logger(send_logs, tags, parameters)
        logger.begin_logging(EPISODE_COUNT, steps_per_ep)
        add_noise = True

        for i in tqdm.trange(EPISODE_COUNT):
            if i >= EPISODE_COUNT * 4 / 5:
                add_noise = False

            cumulative_reward = 0

            obs = self.env.reset()
            obs = np.reshape(obs, (history_length, 1, 2))

            for step in range(steps_per_ep):
                self.debug = obs
                self.actions = agent.act(obs, add_noise)
                next_obs, reward, done = self.env.step(self.actions[0])

                # obs = np.reshape(obs, (history_length, 1, 2))

                agent.step(obs, self.actions, reward, next_obs, done, 1)

                cumulative_reward += np.mean(reward)

                logger.log_round(self.actions[0], reward, cumulative_reward, agent.get_loss(), i * steps_per_ep + step)

                obs = np.reshape(next_obs, (history_length, 1, 2))

                if done:
                    break

            self.env.reset()
            agent.reset()
            logger.log_episode(cumulative_reward, obs[-1, 0], i)

        logger.end()
        print("Training finished.")
        return logger


# class AlreadyRunningException(Exception):
#     def __init__(self, *args, **kwargs):
#         return super().__init__(*args, **kwargs)


# class EnvWrapper:
#     def __init__(self, no_threads, env_constructor, **params):
#         self.params = params
#         self.commands = self._craft_commands(params)
#
#         self.SCRIPT_RUNNING = False
#         self.envs = []
#
#         self.run()
#         for port in self.ports:
#             env = env_constructor()
#             self.envs.append(env)
#
#         self.SCRIPT_RUNNING = True
#
#     def run(self):
#         if self.SCRIPT_RUNNING:
#             raise AlreadyRunningException("Script is already running")
#
#         for cmd, port in zip(self.commands, self.ports):
#             subprocess.Popen(['bash', '-c', cmd])
#         self.SCRIPT_RUNNING = True
#
#     def _craft_commands(self, params):
#         command = '../../waf --run "linear-mesh'
#         for key, val in params.items():
#             command += f" --{key}={val}"
#
#         commands = []
#         for p in self.ports:
#             commands.append(command + f' --openGymPort={p}"')
#
#         return commands
#
#     def reset(self):
#         obs = []
#         for env in self.envs:
#             obs.append(env.reset())
#
#         return obs
#
#     def step(self, actions):
#         next_obs, reward, done, info = [], [], [], []
#
#         for i, env in enumerate(self.envs):
#             no, rew, dn, inf = env.step(actions[i].tolist())
#             next_obs.append(no)
#             reward.append(rew)
#             done.append(dn)
#             info.append(inf)
#
#         return next_obs, reward, done, info
#
#     @property
#     def observation_space(self):
#         dim = repr(self.envs[0].observation_space).replace('Box(', '').replace(',)', '')
#         return (self.no_threads, int(dim))
#
#     @property
#     def action_space(self):
#         dim = repr(self.envs[0].action_space).replace('Box(', '').replace(',)', '')
#         return (self.no_threads, int(dim))
#
#     def close(self):
#         time.sleep(5)
#         for env in self.envs:
#             env.close()
#         # subprocess.Popen(['bash', '-c', "killall linear-mesh"])
#
#         self.SCRIPT_RUNNING = False
#
#     def __getattr__(self, attr):
#         for env in self.envs:
#             env.attr()
