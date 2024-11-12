from sklearn import tree

def save_decision_tree(reg, features, output_txt):
    with open(output_txt, 'w') as file:
        file.write(tree.export_text(reg, feature_names=features))
