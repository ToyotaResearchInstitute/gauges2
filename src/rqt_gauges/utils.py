def get_topic_type(node, topic):
    """
    Subroutine for getting the topic type.

    (nearly identical to rostopic._get_topic_type, except it returns rest of name instead of fn)

    :returns: topic type, real topic name, and rest of name referenced
      if the topic points to a field within a topic, e.g. /rosout/msg, ``str, str, str``
    """
    val = node.get_topic_names_and_types()
    matches = [(t, t_types) for t, t_types in val if t == topic or topic.startswith(t + '/')]
    for t, t_types in matches:
        for t_type in t_types:
            if t_type == topic:
                return t_type, None, None
        for t_type in t_types:
            if t_type != '*':
                return t_type, t, topic[len(t):]
    return None, None, None


def _array_eval(field_name, slot_num):
    """
    Array evaluation.

    :param field_name: name of field to index into, ``str``
    :param slot_num: index of slot to return, ``str``
    :returns: fn(msg_field)->msg_field[slot_num]
    """
    def fn(f):
        return getattr(f, field_name).__getitem__(slot_num)
    return fn


def _field_eval(field_name):
    """
    Field evaluation.

    :param field_name: name of field to return, ``str``
    :returns: fn(msg_field)->msg_field.field_name
    """
    def fn(f):
        if (hasattr(f, field_name)):
            return getattr(f, field_name)
    return fn


def generate_field_evals(fields):
    evals = []
    if fields is not None:
        fields = [f for f in fields.split('/') if f]
        for f in fields:
            if '[' in f:
                field_name, rest = f.split('[')
                slot_num = int(rest[:rest.find(']')])
                value = _array_eval(field_name, slot_num)
                if value is not None:
                    evals.append(value)
            else:
                value = _field_eval(f)
                if value is not None:
                    evals.append(value)
    return evals
