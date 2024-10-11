from ck_model.train import train, save_best_model
import torch


if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    best_accuracy = 90.92

    for i in range(100):
        print(f'-------------- Epoch {i + 1} --------------')
        last_save_epoch, accuracy = train(4, 2, 4, 5000, 0.001 / 2, device)
        print(f'--> accuracy: {accuracy:.2f}%')

        if accuracy >= best_accuracy or accuracy >= 99.6:
            best_accuracy = accuracy
            save_best_model(last_save_epoch, 0)
            print(f'--> model updated')
