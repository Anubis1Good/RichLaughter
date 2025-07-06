import torch
import torch.nn as nn
import torch.optim as optim

class PolicyNetwork(nn.Module):
    def __init__(self, input_size=3, hidden_size=10):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, 3)  # 3 действия: -1, 0, 1
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        probs = self.softmax(self.fc2(x))
        return probs
    
def run_episode(model, states, prices):
    saved_log_probs = []
    rewards = []
    position = 0  # 0 - нет позиции, 1 - лонг, -1 - шорт
    portfolio = []  # Для отслеживания стоимости портфеля

    for i in range(len(states)):
        state = states[i]
        probs = model(torch.FloatTensor(state))
        action = torch.multinomial(probs, 1).item() - 1  # -1, 0, или 1
        saved_log_probs.append(torch.log(probs[0, action + 1]))  # Логарифм вероятности

        # Применяем действие (упрощённая логика)
        if action == 1 and position != 1:  # Лонг
            if position == -1:
                rewards.append(prices[i] - prices[i-1])  # Закрываем шорт
            position = 1
        elif action == -1 and position != -1:  # Шорт
            if position == 1:
                rewards.append(prices[i-1] - prices[i])  # Закрываем лонг
            position = -1

    # Финальная награда = сумма всех PnL
    total_reward = sum(rewards)
    return saved_log_probs, total_reward

def update_policy(saved_log_probs, total_reward, optimizer):
    policy_loss = []
    for log_prob in saved_log_probs:
        # Чем выше награда, тем сильнее "подталкиваем" выбранные действия
        policy_loss.append(-log_prob * total_reward)  # Минимизируем отрицательную награду

    optimizer.zero_grad()
    total_loss = torch.stack(policy_loss).sum()
    total_loss.backward()
    optimizer.step()

model = PolicyNetwork()
optimizer = optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    saved_log_probs, total_reward = run_episode(model, states, prices)
    update_policy(saved_log_probs, total_reward, optimizer)
    print(f"Эпизод {epoch}, Прибыль: {total_reward}")