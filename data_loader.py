def load_data(file_path):
    texts, labels = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) == 2:
                text, label = parts
                texts.append(text)
                labels.append(label)
    return texts, labels
