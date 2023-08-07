# ai-replication

## Checkout at: **https://pypi.org/manage/project/aireplication/releases/**

## Usage
```python
from aireplication.ultils.data import TimeSeriesGenerator, Dataset

config = {"dataset_name": "GYEONGGI2955",
          "features": ["Amount of Consumption", "Temperature"],
          "prediction_feature": "Amount of Consumption",  # Feature to use for prediction
          "input_width": 168,
          "output_length": 1,
          "train_ratio": 0.9
          }

dataset = Dataset(dataset_name=config["dataset_name"])
# data = dataset.dataloader.export_a_single_sequence()
data = dataset.dataloader.export_the_sequence(config["features"])

print("Building time series generator...")
tsf = TimeSeriesGenerator(data=data,
                          config=config,
                          normalize_type=1,
                          shuffle=False)

# Get model 
model = get_model(model_name=args.model_name,
                  config=config)

# Train model
history = model.fit(x=tsf.data_train[0],  # [number_recoder, input_len, number_feature]
                    y=tsf.data_train[1],  # [number_recoder, output_len, number_feature]
                    validation_data=tsf.data_valid)
```

## List of dataset is available
```yaml
config1 = {"dataset_name": "GYEONGGI2955",
          "features": ["Amount of Consumption", "Temperature"],
          "prediction_feature": "Amount of Consumption",  # Feature to use for prediction
          "input_width": 168,
          "output_length": 1,
          "train_ratio": 0.9
          }

config2 = {"dataset_name": "CNU_ENGINEERING_7",
          "features": [ "temperatures", "humidity", "pressure","energy" ]  # Features to use for training
          prediction_feature: "energy",  # Feature to use for prediction
          "input_width": 168,
          "output_length": 1,
          "train_ratio": 0.9
          }
```
## Publishing the package
```shell
pip install twine
python setup.py sdist
twine upload dist/*
```

**- Note: Testing case:**
```shell
twine upload --repository testpypi dist/*
```