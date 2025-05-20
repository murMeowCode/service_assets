from collections import defaultdict
from pygost import gost28147
import secrets

point_coords = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 9: (2, 2)
}

def PSP(number):
    key = secrets.token_bytes(32)
    sbox = "id-Gost28147-89-CryptoPro-A-ParamSet"
    random_bytes = gost28147.encrypt(key=key, ns=(1, 1), sbox=sbox)
    return (random_bytes[1] % number) + 1

class LotPassword():
    def __init__(self):
        self.all_path = self.generate_all_paths()
        self.inp_seq = None
        self.key = None

    def get_key(self):
        pos = PSP(len(self.all_path))
        return self.all_path[pos]
    
    # Функция проверки соседства
    def are_neighbors(self, p1, p2):
        x1, y1 = point_coords[p1]
        x2, y2 = point_coords[p2]
        return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1


    # Функция для генерации всех возможных комбинаций
    def generate_all_paths(self,length=6, gap=1):
        # Сначала создаем словарь соседей для каждой точки
        neighbors = defaultdict(list)
        for p1 in point_coords:
            for p2 in point_coords:
                if p1 != p2 and self.are_neighbors(p1, p2):
                    neighbors[p1].append(p2)
        
        # Рекурсивная функция для построения путей
        def backtrack(path):
            if len(path) == length:
                # Проверяем условие повторения через gap элементов
                valid = True
                for i in range(len(path)):
                    for j in range(i+1, len(path)):
                        if path[i] == path[j] and j - i - 1 < gap:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    results.append(path.copy())
                return
            
            current = path[-1]
            for neighbor in neighbors[current]:
                # Проверяем, можно ли добавить этого соседа
                # Учитываем условие повторения через gap элементов
                if len(path) >= gap + 1:
                    # Если текущий элемент равен тому, что был gap+1 позиций назад
                    if neighbor == path[-(gap+1)]:
                        path.append(neighbor)
                        backtrack(path)
                        path.pop()
                    elif neighbor not in path[-(gap):]:  # Не повторялся в последних gap элементах
                        path.append(neighbor)
                        backtrack(path)
                        path.pop()
                else:
                    path.append(neighbor)
                    backtrack(path)
                    path.pop()
        
        results = []
        # Запускаем для каждой начальной точки
        for start in point_coords:
            backtrack([start])
        
        return results


    def check_sequences(self, secret, user_input):
        if secret == user_input:
            return 1
        
        if secret[:6] == user_input[:6]:
            if secret[-1] != user_input[-1]:
                return 2
        
        if secret[:5] == user_input[:5]:
            if secret[5:] != user_input[5:]:
                return 3
        
        # Проверка 2 подряд в любом месте
        for i in range(len(secret)-1):
            for j in range(len(user_input)-1):
                if secret[0] == user_input[0]:
                    if secret[-1] == user_input[-1]:
                        return 4
        
        return 0


