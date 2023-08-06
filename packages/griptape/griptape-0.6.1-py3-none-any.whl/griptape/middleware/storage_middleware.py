from griptape.middleware import BaseMiddleware


class StorageMiddleware(BaseMiddleware):
    def process_output(self, value: any) -> any:
        print("StorageMiddleware.process_output")
        return value
