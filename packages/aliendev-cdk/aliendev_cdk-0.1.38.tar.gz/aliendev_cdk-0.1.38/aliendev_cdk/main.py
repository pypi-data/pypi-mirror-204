import typer
from aliendev_cdk.service import loginService, registerService, templateService, deployService, logoutService

app = typer.Typer()

@app.command("register")
def register():
    registerService.register()
    
@app.command("login")
def login():
    loginService.login()

@app.command("logout")
def logout():
    logoutService.logout()

@app.command("init")
def initTemplate():
    name = input("Application Name: ")
    new_name = name.replace("-","_").replace(" ","_")
    templateService.init(new_name)

@app.command("deploy")
def deploy():
    deploy = deployService.Deployment()
    deploy.checking_account()
    deploy.read()
    pass

if __name__ == "__main__":
    app()