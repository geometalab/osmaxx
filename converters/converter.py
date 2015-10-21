class Options:
    def __init__(self, output_formats):
        self.output_formats = output_formats

    def get_output_formats(self):
        return self.output_formats

    def __add__(self, other):
        return Options(output_formats=self.output_formats + other.output_formats)
