import ast

class Query:
    def __init__(self, query_string):
        self.query_string = query_string
    
    def to_mongo_query(self):
        # Parse the query string using the ast module
        tree = ast.parse(self.query_string)
        
        # Transform the AST to a MongoDB query
        q = self._transform(tree.body[0].value)
        return q
    
    def _transform(self, node):
        if isinstance(node, ast.BoolOp):
            op = '$and' if isinstance(node.op, ast.And) else '$or'
            return {op: [self._transform(n) for n in node.values]}
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return {'$not': self._transform(node.operand)}
        elif isinstance(node, ast.Compare):
            left = self._transform(node.left)
            right = self._transform(node.comparators[0])
            op_map = {
                ast.Eq: '$eq',
                ast.NotEq: '$ne',
                ast.Lt: '$lt',
                ast.LtE: '$lte',
                ast.Gt: '$gt',
                ast.GtE: '$gte',
                ast.In: '$regex',
                ast.NotIn: '$nin'
            }
            op = op_map[type(node.ops[0])]
            if op == '$regex':
                if isinstance(right, list):
                    return {left: {'$in': right}}
                return {right: {op: f'.*{left}.*'}}
            elif isinstance(node, ast.Compare) and isinstance(node.ops[0], ast.NotIn):
                left = self._transform(node.left)
                #right = [self._transform(value) for value in node.comparators]
                return {right: {'$not': {'$regex': '|'.join(left)}}}
            elif isinstance(right, list):
                return {left: {op: right}}
            else:
                return {left: {op: [right]}}
        # elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Invert):
        #     return {'$regex': self._transform(node.operand)}
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.List):
            return [self._transform(n) for n in node.elts]
        elif isinstance(node, ast.Call):
            if node.func.id == 'exists':
                return { node.args[0].id: {'$exists': True}}
        else:
            raise ValueError(f'Unsupported node type: {type(node)}')