import pandas as pd

from argil.producers.base import BaseProducer


class PandasProducer(BaseProducer):
    def __init__(self):
        pass

    def produce(self, record):
        agent_data = record.observed_agent_data

        complete_list = []
        for i, step in enumerate(agent_data):
            for j, agent in enumerate(step):
                agent["_step"] = i
                agent["_agent"] = j
                complete_list.append(agent)
        df = pd.DataFrame(complete_list)
        df.set_index(["_step", "_agent"], inplace=True)
        df.index.names = ["step", "agent"]
        return df

