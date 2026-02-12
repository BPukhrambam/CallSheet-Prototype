from fastapi import Depends, Form, Request, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app import app, templates, mail
from app.models import User, Project, Role, Skill, UserToSkill, UserToProjectToRole
from app.dependencies import get_current_user, get_db
from flask_mail import Message


@app.get("/", response_class=HTMLResponse)
async def base(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = db.query(Project).all()
    your_projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    return templates.TemplateResponse("base.html", {
        "request": request,
        "title": "Home",
        "projects": projects,
        "user": current_user,
        "your_projects": your_projects
    })


@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if user_id:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    skills = db.query(Skill).all()
    return templates.TemplateResponse("register.html", {
        "request": request,
        "title": "Register",
        "skills": skills
    })


@app.post("/register", response_class=HTMLResponse)
async def register_post(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    pronouns: str = Form(...),
    email: str = Form(...),
    phone: int = Form(...),
    major: str = Form(...),
    minor: str = Form(default=""),
    grad_year: int = Form(...),
    password: str = Form(...),
    skills: list[int] = Form(default=[]),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")
    if user_id:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    existing_user = db.query(User).filter(User.email == email.upper()).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "title": "Register",
            "error": "User already exists."
        })
    
    new_user = User(
        first_name=first_name.upper(),
        last_name=last_name.upper(),
        pronouns=pronouns.upper(),
        email=email.upper(),
        phone=phone,
        major=major.upper(),
        minor=minor.upper(),
        grad_year=grad_year
    )
    new_user.set_password(password)
    new_user.set_username(email.upper())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    for skill_id in skills:
        new_u2s = UserToSkill(user_id=new_user.id, skill_id=skill_id)
        db.add(new_u2s)
    db.commit()
    
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    user_id = request.cookies.get("user_id")
    if user_id:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Sign In"
    })


@app.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(default=False),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email.upper()).first()
    if user is None or not user.check_password(password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Sign In",
            "error": "Invalid email or password"
        })
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=str(user.id), max_age=2592000 if remember_me else None)
    return response


@app.get("/new_project", response_class=HTMLResponse)
async def new_project_get(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roles = db.query(Role).all()
    return templates.TemplateResponse("new_project.html", {
        "request": request,
        "title": "Create New Project",
        "roles": roles
    })


@app.post("/new_project", response_class=HTMLResponse)
async def new_project_post(
    request: Request,
    name: str = Form(...),
    filming_dates: str = Form(...),
    description: str = Form(...),
    roles_needed: list[int] = Form(default=[]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = Project(
        name=name.upper(),
        filming_dates=filming_dates,
        description=description.upper(),
        user_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    for role_id in roles_needed:
        new_u2p2r = UserToProjectToRole(
            user_id=current_user.id,
            project_id=project.id,
            role_id=role_id
        )
        db.add(new_u2p2r)
    db.commit()
    
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.get("/user/{username}", response_class=HTMLResponse)
async def user_profile(
    username: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_name = f"{user.first_name} {user.last_name}"
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    
    return templates.TemplateResponse("user_profile.html", {
        "request": request,
        "title": user_name,
        "user": user,
        "user_name": user_name,
        "project_list": projects
    })


@app.post("/user/{username}/contact", response_class=HTMLResponse)
async def send_contact_message(
    username: str,
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    msg = Message(
        subject=f'You got a message from {email}',
        sender='cs205testingfall23@gmail.com',
        cc=[email],
        recipients=[user.email]
    )
    msg.body = message
    mail.send(msg)
    
    return templates.TemplateResponse("user_profile.html", {
        "request": request,
        "title": f"{user.first_name} {user.last_name}",
        "user": user,
        "user_name": f"{user.first_name} {user.last_name}",
        "project_list": db.query(Project).filter(Project.user_id == user.id).all(),
        "success": "Message was sent!"
    })


@app.get("/project/{project_id}", response_class=HTMLResponse)
async def project_display(
    project_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    creator = db.query(User).filter(User.id == project.user_id).first()
    roles_needed = db.query(UserToProjectToRole).filter(
        UserToProjectToRole.project_id == project.id
    ).all()
    
    roles_needed_list = []
    for role_rel in roles_needed:
        role = db.query(Role).filter(Role.id == role_rel.role_id).first()
        if role:
            roles_needed_list.append(role.title)
    
    return templates.TemplateResponse("project.html", {
        "request": request,
        "title": project.name,
        "creator": creator,
        "roles_needed_list": roles_needed_list,
        "project": project
    })


@app.get("/project_search", response_class=HTMLResponse)
async def project_search(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = db.query(Project).all()
    roles = db.query(Role).all()
    
    return templates.TemplateResponse("project_search.html", {
        "request": request,
        "projects": projects,
        "roles": roles
    })


@app.post("/project_search", response_class=HTMLResponse)
async def project_search_post(
    request: Request,
    search_by: str = Form(...),
    project_name: str = Form(default=""),
    project_role: int = Form(default=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if search_by == "name" and project_name:
        return RedirectResponse(
            url=f"/project_search_result_name/{project_name.upper()}",
            status_code=status.HTTP_302_FOUND
        )
    elif search_by == "role" and project_role:
        return RedirectResponse(
            url=f"/project_search_result_role/{project_role}",
            status_code=status.HTTP_302_FOUND
        )
    
    return RedirectResponse(url="/project_search", status_code=status.HTTP_302_FOUND)


@app.get("/project_search_result_name/{name}", response_class=HTMLResponse)
async def project_search_result_name(
    name: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = db.query(Project).filter(Project.name == name).all()
    
    results = []
    for project in projects:
        creator = db.query(User).filter(User.id == project.user_id).first()
        results.append({"project": project, "creator": creator})
    
    return templates.TemplateResponse("project_search_result.html", {
        "request": request,
        "query": name,
        "results": results
    })


@app.get("/project_search_result_role/{role}", response_class=HTMLResponse)
async def project_search_result_role(
    role: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role_obj = db.query(Role).filter(Role.id == role).first()
    if not role_obj:
        raise HTTPException(status_code=404, detail="Role not found")
    
    result_ids = db.query(UserToProjectToRole).filter(
        UserToProjectToRole.role_id == role
    ).all()
    
    results = []
    for result_id in result_ids:
        project = db.query(Project).filter(Project.id == result_id.project_id).first()
        if project:
            creator = db.query(User).filter(User.id == project.user_id).first()
            results.append({"project": project, "creator": creator})
    
    return templates.TemplateResponse("project_search_result.html", {
        "request": request,
        "query": role_obj.title,
        "results": results,
        "role_title": role_obj.title
    })


@app.get("/profile_search", response_class=HTMLResponse)
async def profile_search(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skills = db.query(Skill).all()
    return templates.TemplateResponse("profile_search.html", {
        "request": request,
        "skills": skills
    })


@app.post("/profile_search", response_class=HTMLResponse)
async def profile_search_post(
    request: Request,
    search_by: str = Form(...),
    profile_name: str = Form(default=""),
    profile_skill: int = Form(default=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if search_by == "name" and profile_name:
        return RedirectResponse(
            url=f"/user/{profile_name.upper()}",
            status_code=status.HTTP_302_FOUND
        )
    elif search_by == "skill" and profile_skill:
        return RedirectResponse(
            url=f"/profile_search_result_skill/{profile_skill}",
            status_code=status.HTTP_302_FOUND
        )
    
    return RedirectResponse(url="/profile_search", status_code=status.HTTP_302_FOUND)


@app.get("/profile_search_result_skill/{query}", response_class=HTMLResponse)
async def profile_search_result_skill(
    query: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.id == query).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    user_to_skills = db.query(UserToSkill).filter(UserToSkill.skill_id == skill.id).all()
    user_list = []
    for u2s in user_to_skills:
        user = db.query(User).filter(User.id == u2s.user_id).first()
        if user:
            user_list.append(user.username)
    
    return templates.TemplateResponse("profile_search_result_skill.html", {
        "request": request,
        "title": "Profile Search by Skill",
        "skill_title": skill.title,
        "user_list": user_list
    })


@app.get("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user_id")
    return response


@app.get("/reset_db")
async def reset_db(db: Session = Depends(get_db)):
    # Delete all data
    db.query(UserToSkill).delete()
    db.query(UserToProjectToRole).delete()
    db.query(Project).delete()
    db.query(User).delete()
    db.query(Skill).delete()
    db.query(Role).delete()
    db.commit()
    
    # Repopulate with dummy data
    skills = [
        Skill(title="DIRECTING"), Skill(title="PRODUCING"), Skill(title="SOUND"),
        Skill(title="EDITING"), Skill(title="MUSIC"), Skill(title="WRITING"),
        Skill(title="ACTING"), Skill(title="SINGING"), Skill(title="LIGHTING")
    ]
    for skill in skills:
        db.add(skill)
    
    roles = [
        Role(title="DIRECTOR"), Role(title="PRODUCER"),
        Role(title="1ST ASSISTANT DIRECTOR"), Role(title="2ND ASSISTANT DIRECTOR"),
        Role(title="ASSISTANT PRODUCER"), Role(title="DIRECTOR OF PHOTOGRAPHY"),
        Role(title="1ST ASSISTANT CAMERA"), Role(title="2ND ASSISTANT CAMERA"),
        Role(title="CAMERA OPERATOR"), Role(title="SCRIPT SUPERVISOR"),
        Role(title="PRODUCTION ASSISTANT"), Role(title="EDITOR"),
        Role(title="ASSISTANT EDITOR"), Role(title="SOUND MIXER"),
        Role(title="BOOM OPERATOR"), Role(title="PRODUCTION DESIGNER"),
        Role(title="SET PHOTOGRAPHER"), Role(title="SOCIAL MEDIA MANAGER"),
        Role(title="GAFFER"), Role(title="KEY GRIP"), Role(title="GRIP"),
        Role(title="LIGHTING TECHNICIAN"), Role(title="HAIR & MAKEUP"),
        Role(title="CHOREOGRAPHER"), Role(title="WRITER"), Role(title="COLORIST"),
        Role(title="COMPOSER"), Role(title="DIGITAL IMAGING TECHNICIAN"),
        Role(title="PROPERTY MASTER"), Role(title="CASTING DIRECTOR"),
        Role(title="LOCATION MANAGER")
    ]
    for role in roles:
        db.add(role)
    
    db.commit()
    
    projects = [
        Project(name="MANEATER", filming_dates="11/10/23", description="SUCH A GOOD FILM", user_id=1),
        Project(name="HARMONY OF HEARTS", filming_dates="12/2/23", description="SUCH A GOOD FILM", user_id=1),
        Project(name="TRUTH SEEKER", filming_dates="8/10/23", description="SUCH A GOOD FILM", user_id=1),
        Project(name="STARLIGHT DREAMS", filming_dates="7/15/23", description="A CAPTIVATING ROMANCE", user_id=1),
        Project(name="MYSTERIOUS SHADOWS", filming_dates="6/5/23", description="A THRILLING MYSTERY", user_id=1),
        Project(name="SUNSET SERENADE", filming_dates="9/20/23", description="A HEARTWARMING MUSICAL", user_id=1),
        Project(name="ETERNAL ECLIPSE", filming_dates="4/1/23", description="A DARK FANTASY EPIC", user_id=1),
        Project(name="LOST IN TIME", filming_dates="2/12/23", description="A TIME-TRAVEL ADVENTURE", user_id=1),
        Project(name="ENCHANTED GARDEN", filming_dates="10/8/23", description="A MAGICAL FAMILY FILM", user_id=1),
        Project(name="UNCHARTED WATERS", filming_dates="3/25/23", description="A HIGH-SEAS ADVENTURE", user_id=1),
        Project(name="BEYOND THE STARS", filming_dates="5/30/23", description="AN INTERGALACTIC JOURNEY", user_id=1),
        Project(name="WHISPERS IN THE WOODS", filming_dates="11/18/23", description="A HAUNTING HORROR", user_id=1),
        Project(name="CELESTIAL HARMONY", filming_dates="7/5/23", description="A SCI-FI ODYSSEY", user_id=1),
        Project(name="SERENADE UNDER THE MOON", filming_dates="1/9/23", description="A ROMANTIC COMEDY", user_id=1),
        Project(name="THE LOST KINGDOM", filming_dates="8/27/23", description="AN EPIC FANTASY QUEST", user_id=1),
        Project(name="CITY OF ILLUSIONS", filming_dates="6/18/23", description="A PSYCHOLOGICAL THRILLER", user_id=1),
        Project(name="CHASING DREAMS", filming_dates="9/12/23", description="A DRAMA OF AMBITIONS", user_id=1),
        Project(name="SECRET OF THE ORACLE", filming_dates="4/28/23", description="A MYSTICAL ADVENTURE", user_id=1),
        Project(name="STARDUST MEMORIES", filming_dates="2/5/23", description="A NOSTALGIC JOURNEY", user_id=1),
        Project(name="UNDERGROUND REBELLION", filming_dates="10/15/23", description="A DYSTOPIAN ACTION", user_id=1),
        Project(name="WHEN SHADOWS FALL", filming_dates="5/8/23", description="A SUPERNATURAL MYSTERY", user_id=1),
        Project(name="LOVE IN BLOOM", filming_dates="12/7/23", description="A ROMANTIC DRAMA", user_id=1),
        Project(name="THE TIMELESS VOYAGE", filming_dates="8/3/23", description="A TIME-TRAVEL ROMANCE", user_id=1),
    ]
    for proj in projects:
        db.add(proj)
    
    db.commit()
    
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
