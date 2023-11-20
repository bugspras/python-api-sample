from app import app
from flask import jsonify
from flask import flash, request
from config import conn,mariadb

cursor = conn.cursor()
contacts = []
@app.route('/create', methods=['POST'])
def create_emp():
    try:        
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']	
        if _name and _email and _phone and _address and request.method == 'POST':
            sqlQuery = "INSERT INTO emp(name, email, phone, address) VALUES(?, ?, ?, ?)"
            bindData = (_name, _email, _phone, _address)            
            try:
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                respone = jsonify('Employee added successfully!')
                respone.status_code = 200
                return respone
            except mariadb.Error as e:
                print(f"Error: {e}")
        else:
            return showMessage()
    except Exception as e:
        print(e)      
     
@app.route('/emp')
def emp():
    try:
        try:
            cursor.execute("SELECT id, name, email, phone, address FROM emp")
            data = []
            row_header = [x[0] for x in cursor.description]

            # empRows = cursor.fetchall()
            # for result in empRows:
            #     data.append(dict(zip(row_header, result)))
            
            data.append([dict(zip(row_header, result)) for result in cursor.fetchall()])
            
            message = {
                'status': True,
                'emp': data,
            }
            respone = jsonify(message)
            respone.status_code = 200
            return respone
        except mariadb.Error as e:
            print(f"Error: {e}")
    except Exception as e:
        print(e)

@app.route('/emp/<int:id>')
def detail(id):
    try:
        try:
            cursor.execute("SELECT id, name, email, phone, address FROM emp WHERE id =?", (id,))
            # empRow = cursor.fetchone()
            # respone = jsonify(empRow)
            data = []
            row_header = [x[0] for x in cursor.description]
            data.append([dict(zip(row_header, result)) for result in cursor.fetchmany()])
            
            message = {
                'status': True,
                'emp': data,
            }
            respone = jsonify(message)
            respone.status_code = 200
            return respone
        except mariadb.Error as e:
            print(f"Error: {e}")
    except Exception as e:
        print(e)

@app.route('/update', methods=['PUT'])
def update_emp():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        if _name and _email and _phone and _address and _id and request.method == 'PUT':			
            sqlQuery = "UPDATE emp SET name=?, email=?, phone=?, address=? WHERE id=?"
            bindData = (_name, _email, _phone, _address, _id,)
            try:
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                respone = jsonify('Employee updated successfully!')
                respone.status_code = 200
                return respone
            except mariadb.Error as e:
                print(f"Error: {e}")
        else:
            return showMessage()
    except Exception as e:
        print(e)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_emp(id):
    try:
        try:
            cursor.execute("DELETE FROM emp WHERE id =?", (id,))
            conn.commit()
            respone = jsonify('Employee deleted successfully!')
            respone.status_code = 200
            return respone
        except mariadb.Error as e:
            print(f"Error: {e}")
    except Exception as e:
        print(e)
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    conn.close()
    app.run()
