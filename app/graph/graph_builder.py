def insert_file_structure(tx, data):
    file_path = data["file"]

    tx.run("""
        MERGE (f:File {path: $file_path})
    """, file_path=file_path)

    for func in data["functions"]:
        func_id = f"{file_path}:{func}"

        tx.run("""
            MERGE (fn:Function {id: $id})
            SET fn.name = $name, fn.file = $file
            WITH fn
            MATCH (f:File {path: $file})
            MERGE (f)-[:CONTAINS]->(fn)
        """, id=func_id, name=func, file=file_path)

    for cls in data["classes"]:
        cls_id = f"{file_path}:{cls}"

        tx.run("""
            MERGE (c:Class {id: $id})
            SET c.name = $name, c.file = $file
            WITH c
            MATCH (f:File {path: $file})
            MERGE (f)-[:CONTAINS]->(c)
        """, id=cls_id, name=cls, file=file_path)

    for caller, callee in data["calls"]:
        caller_id = f"{file_path}:{caller}"

        tx.run("""
            MERGE (caller:Function {id: $caller_id})
            MERGE (callee:Function {name: $callee})
            MERGE (caller)-[:CALLS]->(callee)
        """, caller_id=caller_id, callee=callee)

    for child, parent in data["inheritance"]:
        tx.run("""
            MERGE (c1:Class {name: $child})
            MERGE (c2:Class {name: $parent})
            MERGE (c1)-[:INHERITS]->(c2)
        """, child=child, parent=parent)