from ultralytics import YOLO, checks, hub
checks()

hub.login('d5dacce67251559e250de7affd15dae6cbb4b5c798')

model = YOLO('https://hub.ultralytics.com/models/8tWAXmazcyxdq0eTy5nt')
results = model.train(amp=False)