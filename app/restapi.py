import json
import pandas as pd
from io import StringIO
from flask import Flask, request
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
app = Flask(__name__)


@app.route('/pca', methods=['POST'])
def process_pca_request():

    csv_data = request.get_data(as_text=True)
    csv_string = StringIO(csv_data)

    # default number of dimensions for PCA is 2
    pca_dims = 2

    pca_dims_arg = request.args.get("dims")
    if pca_dims_arg is not None:
        pca_dims = int(pca_dims_arg)

    print("dims: ", pca_dims)

    # load dataset into dataframe
    # header=1 means treat first row as column names
    df = pd.read_csv(csv_string, header=0)

    print(df[:2])

    cols = df.columns.values.tolist()
    print("columns: ", cols)

    features = cols[1:]
    target_column = cols[0]

    print("features: ", features)
    print("target: ", target_column)

    # Separating out the features
    x = df.loc[:, features].values

    # Separating out the target
    y = df.loc[:, [target_column]].values

    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=pca_dims)

    pca_component_names = []

    if pca_dims == 2:
        pca_component_names = ['pc1', 'pc2']
    elif pca_dims == 3:
        pca_component_names = ['pc1', 'pc2', 'pc3']
    else:
        raise "Unsupported dimension " + pca_dims

    principal_components = pca.fit_transform(x)
    principal_df = pd.DataFrame(data=principal_components, columns=pca_component_names)

    result_df = pd.concat([principal_df, df[[target_column]]], axis=1)

    # turn dataframe into JSON string
    result_json_str = result_df.to_json(orient="records")

    # turn JSON string into JSON object
    result_json = json.loads(result_json_str)

    return json.dumps({"success": True, "pca_components": result_json })


app.run(host='0.0.0.0', port=7000)
