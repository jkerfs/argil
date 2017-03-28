from collections import namedtuple

Record = namedtuple("Record", ["observed_agent_data", "glance_agent_data", "glance_object_data", "env_data"])


class RecordSimulation:
    def __init__(self, glance, observe, survey, num_steps=10, inc=1):
        self.glance = glance
        self.observe = observe
        self.survey = survey
        self.num_steps = num_steps
        self.inc = inc

    def run(self, env):
        env.reset()

        step_ind = 0
        observed_agent_data = []
        glance_object_data = [self.glance(obj) for obj in env.objects]
        glance_agent_data = [self.glance(agent) for agent in env.agents]
        env_data = self.survey(env)

        while True:
            step_ind += 1
            for i in range(self.inc):
                done = env.step()
                if done:
                    break
            observed_agent_data.append([self.observe(agent) for agent in env.agents])

            if (self.num_steps and step_ind > self.num_steps) or done:
                break
        return Record(observed_agent_data, glance_agent_data, glance_object_data, env_data)


