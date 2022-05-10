
import pyarrow as pa
import pyarrow.flight as fl
import pickle as pkl
import pandas as pd
import numpy as np

class FlightServer(fl.FlightServerBase):

    def __init__(self, location="grpc://0.0.0.0:8815", **kwargs):
        super(FlightServer, self).__init__(location, **kwargs)
        self.loaded_model = pkl.load(open("model", 'rb'))

        self.tables = {}

    def do_get(self, context, ticket):
        table = self.tables[ticket.ticket]
        return fl.RecordBatchStream(table)
        # return fl.GeneratorStream(table.schema, table.to_batches(max_chunksize=1024))

    def do_put(self, context, descriptor, reader, writer):
        ticket_name = b''.join(descriptor.path)
        self.tables[ticket_name] = reader.read_all()

    def get_flight_info(self, context, descriptor):
        ticket_name = b''.join(descriptor.path)
        if ticket_name in self.tables:
            table = self.tables[ticket_name]
            endpoints = [fl.FlightEndpoint(ticket_name, ["grpc://0.0.0.0:8815"])]
            return fl.FlightInfo(table.schema, descriptor, endpoints, table.num_rows, 0)

        raise KeyError("Unknown ticket name: {}".format(ticket_name))

    def get_schema(self, context, descriptor):
        info = self.get_flight_info(context, descriptor)
        return fl.SchemaResult(info.schema)

    def list_flights(self, context, criteria):
        for ticket_name in self.tables:
            descriptor = fl.FlightDescriptor.for_path(ticket_name)
            yield self.get_flight_info(context, descriptor)

    def list_actions(self, context):
        return [("greet", "returns greeting"), ("score", "returns score"), ("prime", "returns prime")]


    def _score(self, data):
        return pd.DataFrame(self.loaded_model.predict(data))

    def _prime(self, c1):

        def largest_prime_factor(n):
            i = 2
            while i * i <= n:
                if n % i:
                    i += 1
                else:
                    n //= i
            return n

        vlpf = np.vectorize(largest_prime_factor)

        return pd.DataFrame(vlpf(c1))

    def do_action(self, context, action):
        if action.type == "greet":
            yield pa.flight.Result(b'Hello!')
        elif action.type == "score":
            scored_df = self._score(self.tables[b'scoreit'].to_pandas())
            scored = pa.Table.from_pandas(scored_df)
            self.tables[b'scored'] = scored
            yield pa.flight.Result(bytes([0]))
        elif action.type == "prime":
            scored_df = self._prime(self.tables[b'scoreit'].to_pandas().values)
            scored = pa.Table.from_pandas(scored_df)
            self.tables[b'scored'] = scored
            yield pa.flight.Result(bytes([0]))
        else:
            raise NotImplementedError("Unknown action: {}".format(action.type))


def main():
    FlightServer().serve()

if __name__ == '__main__':
    main()
