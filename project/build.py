from model.components import Builder

# Create model with Builder
builder = Builder()
model = builder.CreateDummyModel()
builder.BuildModel(model)
