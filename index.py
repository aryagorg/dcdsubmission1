from flask import Flask,Response,request,render_template,redirect,jsonify
from datetime import datetime
import app  
import pyodbc

app = Flask(__name__)


@app.route('/form', methods=['GET'])
def show():

    html = """<HTML>
    <head>
        <title>Registration</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.css">
        <link rel="stylesheet" href="https://cdn.datatables.net/1.10.19/css/dataTables.bootstrap4.min.css">
    </head>
    <body>
        <h1></h1>
        <div class="container">
        <div class="row justify-content-center">
            <div class="col-12 col-md-8 col-lg-6 pb-5">


                <!--Form with header-->

                <form action="doform" method="POST">
                    <div class="card border-primary rounded-0">
                        <div class="card-header p-0">
                            <div class="bg-info text-white text-center py-2">
                                <h3><i class="fa fa-envelope"></i>Register here!</h3>
                                <p class="m-0">Fill the form below.</p>
                            </div>
                        </div>
                        <div class="card-body p-3">

                            <!--Body-->
                            <div class="form-group">
                                <div class="input-group mb-2">
                                    <div class="input-group-prepend">
                                        <div class="input-group-text"><i class="fa fa-user text-info"></i></div>
                                    </div>
                                    <input type="text" class="form-control" id="nombre" name="name"
                                        placeholder="Your name" required>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="input-group mb-2">
                                    <div class="input-group-prepend">
                                        <div class="input-group-text"><i class="fa fa-envelope text-info"></i></div>
                                    </div>
                                    <input type="email" class="form-control" id="nombre" name="email"
                                        placeholder="example@gmail.com" required>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="input-group mb-2">
                                    <div class="input-group-prepend">
                                        <div class="input-group-text"><i class="fa fa-envelope text-info"></i></div>
                                    </div>
                                    <input type="text" class="form-control" id="nombre" name="designation"
                                        placeholder="Your designation <eg:engineer>" required>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="input-group mb-2">
                                    <div class="input-group-prepend">
                                        <div class="input-group-text"><i class="fa fa-envelope text-info"></i></div>
                                    </div>
                                    <input type="text" class="form-control" id="nombre" name="company"
                                        placeholder="Your company name" required>
                                </div>
                            </div>

                            <div class="text-center">
                                <input type="submit" value="Submit" class="btn btn-info btn-block rounded-0 py-2">
                            </div>

                            
                        </div>

                    </div>
                </form>
                </div>
            </div>
        </div>

        <table id="example" class="table table-striped table-bordered" style="width:100%">
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Designation</th>
                <th>Company</th>
            </tr>
        </thead>
        <tbody>
            {0}
        </tbody>
        </table>

        <script src="https://code.jquery.com/jquery-3.3.1.js"></script>
        <script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.10.19/js/dataTables.bootstrap4.min.js"></script>
        <script>
            
        </script>
    </body>
    </HTML>""" 

    connection = pyodbc.connect('Driver={SQL Server};Server=dcdappserver.database.windows.net;Database=dicodingdb;uid=dicoding;pwd=Arya1234')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dbo.register")
    data = cursor.fetchall()  
    items = data
    tr = "<tr>{0}</tr>"
    td = "<td>{0}</td>"
    subitems = [tr.format(''.join([td.format(a) for a in item])) for item in items]
    result = html.format("".join(subitems)) # or write, whichever
    connection.close()

    return Response(response = result, status = 200, mimetype = "text/html")

@app.route('/doform', methods=['POST'])
def savedata():
    _name = request.form['name']
    _email = request.form['email']
    _designation = request.form['designation']
    _company = request.form['company']

    sql = "INSERT INTO register(Name, Email, Designation, Company) VALUES('{}', '{}', '{}', '{}')".format(_name, _email, _designation, _company)
    connection = pyodbc.connect('Driver={SQL Server};Server=dcdappserver.database.windows.net;Database=dicodingdb;uid=dicoding;pwd=Arya1234')
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()

    return redirect("https://dcdsubmission1.azurewebsites.net:443/form", code=302)

app.run(host="0.0.0.0", port=443)