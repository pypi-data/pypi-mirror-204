import tensorflow as tf
from ml2_util.MLModel import MLModel
from code_util.markdown import markdowndoc, draw_markdownobj_flowchart, flowchart_color_enum, flowchart_shape_enum


def generate_tfmodel_graph(model: MLModel, path: str):
    md = markdowndoc(path, need_toc=True)
    mk_fc = draw_markdownobj_flowchart(oriented_left2right=False)

    tensor_list = {}

    def _draw_tensor(tensor):
        if tensor.name not in tensor_list:
            tensor_list[tensor.name] = tensor
            mk_fc.add_node(f'"{tensor.shape}"', tensor.name)

    md.write_title("模型图", 1)
    for ly in model.Model_Ref.layers:
        if isinstance(ly, tf.keras.layers.InputLayer):
            continue

        mk_fc.add_node(ly.name, ly.name)
        mk_fc.set_node_shape(ly.name, flowchart_shape_enum.Circle)
        mk_fc.set_node_color(ly.name, flowchart_color_enum.Orange)
        _draw_tensor(ly.input)
        _draw_tensor(ly.output)

        mk_fc.add_line(ly.input.name, ly.name)
        mk_fc.add_line(ly.name, ly.output.name)

    md.write_markdownobj(mk_fc)

    md.write_title("参数表", 1)
    title_list = ["name", "weight_shape", "Trainable"]
    data_list = []

    for ly in model.Model_Ref.layers:
        if isinstance(ly, tf.keras.layers.InputLayer):
            continue
        shapestr = ""
        for ws in ly.weights:
            shapestr += str(ws.shape) + "<br>"

        data_list.append([ly.name, shapestr, str(ly.trainable)])

    md.write_table(title_list, data_list)

    md.flush()
    pass
