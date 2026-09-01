import hashlib
import json


def format_request(body):
    query = body.get('query')
    if not query:
        return None
    
    query_bool = query.get('bool')
    if not query_bool:
        return None
    
    filt = query_bool.get('filter')
    if not filt:
        return None
    
    filter_bool = filt.get('bool')
    if not filter_bool:
        return None
    
    filter_bool_must = filter_bool.get('must')
    if not filter_bool_must:
        return None
    
    other_filters = []
    esql = None
    for f in filter_bool_must:
        if f.get('esql'):
            esql = f['esql']
        else:
            other_filters.append(f)

    if esql:
        new_body = {'filter': {'bool': {'must': other_filters}}, 'query': esql}
        return new_body

    return None


def format_source(col_names, val_row):
    """ Build a document body from one ES|QL result row.

    Returns _source verbatim when the query carries it. Otherwise nests the flat
    columns into a document, dropping the nulls and multi-field columns that would
    make Elasticsearch fail with document_parsing_exception.
    """
    if '_source' in col_names:
        doc = val_row[col_names.index('_source')]
        if isinstance(doc, str):
            doc = json.loads(doc)
        if doc is not None:
            doc = dict(doc)
            # _id and _index arrive as their own columns, not inside _source.
            for name in ('_id', '_index'):
                if name in col_names and val_row[col_names.index(name)] is not None:
                    doc.setdefault(name, val_row[col_names.index(name)])
            return doc

    names = set(col_names)
    source = {}
    for name, value in sorted(zip(col_names, val_row), key=lambda col: col[0].count('.')):
        if value is None:
            continue

        keys = name.split('.')
        # Skip a multi-field: some ancestor path is itself a column. That ancestor
        # may be null, since ignore_above spares .text but not the parent.
        if any('.'.join(keys[:i]) in names for i in range(1, len(keys))):
            continue

        node = source
        for key in keys[:-1]:
            node = node.setdefault(key, {})
        node[keys[-1]] = value

    return source


def format_results(results, default_index=None):
    columns = results.pop('columns', None)
    values = results.pop('values', None)
    if columns is None or values is None:
        return results
    
    col_names = [col['name'] for col in columns]
    hits = []
    for val_row in values:
        doc = format_source(col_names, val_row)
        
        # Pull metadata fields if present
        doc_id = doc.get('_id', None)
        doc_index = doc.get('_index', default_index)
        
        if not doc_id:
            # Generate deterministic hash of the document to use as unique ID
            doc_hash = hashlib.sha256(json.dumps(doc, sort_keys=True, default=str).encode('utf-8')).hexdigest()
            doc_id = doc_hash
            
        hit = {
            '_index': doc_index,
            '_id': doc_id,
            '_source': doc
        }
        hits.append(hit)
        
    results['hits'] = {
        'total': {
            'value': len(values),
            'relation': 'eq'
        },
        'hits': hits
    }
    results['esql'] = True
    return results
