import logging


class Logger:
    logger = None

    def get_logger(self):
        if self.logger is not None:
            return self.logger

        self.logger = logging.getLogger("api-gateway")
        self.logger.setLevel(logging.INFO)

        # Create a formatter with colored log level
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s')

        # Create a file handler

        # Create a stream handler (optional, can be used to output logs to the console)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(stream_handler)

        return self.logger
