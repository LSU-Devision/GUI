

class OysterPage:
    def __init__(self,master):
        self.master = master

    def calculate(self,sample_weight,subsample_weight,predicted_number):
        subsamples_per_sample = sample_weight / subsample_weight
        predicted_total_count = subsamples_per_sample * predicted_number
        return predicted_total_count

