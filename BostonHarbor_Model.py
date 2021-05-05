import torch
import torch.nn as nn
import torch.nn.functional as F


class Encoder(nn.Module):
    def __init__(self, sample_size, condition_size, hidden_size):
        super().__init__()
        self.fc1 = nn.Linear(sample_size + condition_size, hidden_size)
        self.fc2 = nn.Dropout(p = 0.5)
        self.fc3 = nn.Linear(hidden_size, hidden_size)

    def forward(self, x, c):
        x = torch.cat([x, c], 1)
        p_x = F.relu(self.fc1(x))
        p_x = self.fc2(p_x)
        p_x = F.relu(self.fc3(p_x))

        return p_x


class LatentZ(nn.Module):
    def __init__(self, hidden_size, latent_size):
        super().__init__()
        self.mu = nn.Linear(hidden_size, latent_size)
        self.logvar = nn.Linear(hidden_size, latent_size)

    def forward(self, p_x):
        mu = self.mu(p_x)
        logvar = self.logvar(p_x)

        std = torch.exp(0.5*logvar)
        eps = torch.randn_like(std)

        return std * eps + mu, logvar, mu


class Decoder(nn.Module):
    def __init__(self, latent_size, condition_size, hidden_size, sample_size):
        super().__init__()
        self.fc1 = nn.Linear(latent_size + condition_size, hidden_size)
        self.fc2 = nn.Dropout(p = 0.5)

        #self.fc3 = nn.Linear(hidden_size, hidden_size)

        self.fc3 = nn.Linear(hidden_size, 128)
        self.fc4 = nn.Linear(128, sample_size)

    def forward(self, z_x, c):
        z = torch.cat([z_x, c], 1)
        q_x = F.relu(self.fc1(z))
        q_x = self.fc2(q_x)
        q_x = F.relu(self.fc3(q_x))
        #q_x = torch.relu(self.fc3(q_x))
        q_x = self.fc4(q_x)

        return q_x


class CVAE(nn.Module):
    def __init__(self, sample_size, condition_size, hidden_encoder_size, hidden_decoder_size, latent_size=2):
        super().__init__()
        self.sample_size = sample_size
        self.condition_size = condition_size
        self.hidden_encoder_size = hidden_encoder_size
        self.hidden_decoder_size = hidden_decoder_size
        self.latent_size = latent_size

        self.encoder = Encoder(sample_size, condition_size, hidden_encoder_size)
        self.latent_z = LatentZ(hidden_encoder_size, latent_size)
        self.decoder = Decoder(latent_size, condition_size, hidden_decoder_size, sample_size)

    def forward(self, x, c):
        p_x = self.encoder(x, c)
        z, logvar, mu = self.latent_z(p_x)
        q_z = self.decoder(z, c)

        return q_z, logvar, mu, z


def main():
    # Example initialization
    model = CVAE(sample_size         = 10,
                 condition_size      = 100,
                 hidden_encoder_size = 512,
                 hidden_decoder_size = 512,
                 latent_size         = 3)
    print(model)


if __name__ == "__main__":
    main()

