from pyvis.network import Network
from common.llm import embedding
from typing import Any
import pyvis as pv

    
def embed_text(txt:str)->Any| None:
    if txt:
        return embedding.embed_query(txt)
    else:
        return None

def split_dataframe(df, chunk_size = 100):
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks


def visualize_result(query_graph, nodes_text_properties) -> Network:
    visual_graph = pv.network.Network(height='500px', width='500px', heading='',)
    print('helper')
    for node in query_graph.nodes:
        node_label = list(node.labels)[0]
        node_text = node[nodes_text_properties[node_label]]
        visual_graph.add_node(n_id = node.element_id, label= node_text)

    for relationship in query_graph.relationships:
        visual_graph.add_edge(
            relationship.start_node.element_id,
            relationship.end_node.element_id,
            title=relationship.type
        )
    print('helper end')
    return visual_graph
      
if __name__ == "__main__":
    pass