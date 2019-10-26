import numpy as np

from envs import MracEnv
from agents import NullAgent
from utils import load_spec

import fym.logging as logging


def parse_data(env, data):
    xs = data['state']['main_system']
    Ws = data['state']['adaptive_system']

    cmd = np.hstack([env.cmd.get(t) for t in data['time']])
    u_mrac = np.vstack(
        [-W.T.dot(env.unc.basis(x)) for W, x in zip(Ws, xs)])

    data.update({
        "control": {
            "MRAC": u_mrac,
        },
        "cmd": cmd,
    })
    logging.save('data/mrac/history.h5', data)


def main():
    spec = load_spec('spec.json')
    env = MracEnv(spec, data_callback=parse_data)
    agent = NullAgent(env)

    obs = env.reset()

    while True:
        action = agent.act(obs)

        next_obs, reward, done, info = env.step(action)

        if done:
            break

    env.close()


if __name__ == '__main__':
    main()