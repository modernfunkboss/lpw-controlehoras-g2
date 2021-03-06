from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import extract
from datetime import date, datetime
from flask_login import login_required, current_user
from .formLancamentos import lancamentoForm
from . import lancamentos
from app import db
from app.models import Lancamento, Task, Binding

@lancamentos.route('/lancamentos', methods=['GET', 'POST'])
@login_required
def lancamento():
    form = lancamentoForm()
    form.selectProjeto.choices = [(project.project_id, project.project.nameProject) for project in
                                  Binding.query.filter_by(users_id=current_user.id).all()]
    form.selectAtividade.choices = [(task.codTask, task.descricao) for task in Task.getAllTask()]

    if request.method == 'POST' and form.gravar.data == True:
        dateInic = datetime(form.dtInicio.data.year, form.dtInicio.data.month, form.dtInicio.data.day, 
            form.hrInicio.data.hour, form.hrInicio.data.minute, form.hrInicio.data.second)
        print(dateInic)

        dateEnd = datetime(form.dtFim.data.year, form.dtFim.data.month, form.dtFim.data.day, 
            form.hrFim.data.hour, form.hrFim.data.minute, form.hrFim.data.second)
        print(dateEnd)

        if form.validacao(form):
            flash('Falta preenchar um campo!', 'danger')
        elif form.valdDate(dateInic, dateEnd):
            flash('Data ou hora invalida!', 'danger')
        else:
            try:                
                lancam = Lancamento(
                    users_id=current_user.id,
                    project_id=form.selectProjeto.data,
                    dtInic=dateInic.date(),
                    hrInic=dateInic.time(),
                    dtFim=dateEnd.date(),
                    hrFim=dateEnd.time(),
                    task_id=form.selectAtividade.data,
                    descricao=form.descricao.data)
                db.session.add(lancam)
                db.session.commit()
                strTmp = 'Registrado com sucesso - data inicio:' + str(dateInic.date().strftime('%d/%m/%Y')) + ' hora inicio: ' + str(dateInic.time()) + ' data fim: ' + \
                    str(dateEnd.date())  + ' hora fim: ' + str(dateEnd.time())
                flash(strTmp, 'success')
            except:
                db.session.rollback()
                flash('Registro falhou na adição', 'danger')
    elif request.method == 'GET' and request.args.get('delete'):
        if request.args.get('delete') == '':
            flash('Falta a identificacao da tabela!', 'danger')
        else:
            try:
                lancament = Lancamento.query.filter_by(id=request.args.get('delete')).first_or_404()
                db.session.delete(lancament)
                db.session.commit()
                flash('Registro apagado com sucesso', 'info')
            except:
                db.session.rollback()
                flash('Registro falhou em apagar', 'danger')
    elif request.method == 'GET' and request.args.get('update'):
        if request.args.get('update') == '':
            flash('Falta a matricula!', 'danger')
        else:
            i_d_lanc_update = request.args.get('update')
            lancam = Lancamento.query.filter_by(id=i_d_lanc_update).first_or_404()
            form.selectProjeto.process_data(lancam.project_id)
            form.selectAtividade.process_data(lancam.task_id)
            form.dtInicio.data = lancam.dtInic
            form.hrInicio.data = lancam.hrInic
            form.dtFim.data = lancam.dtFim
            form.hrFim.data = lancam.hrFim
            form.descricao.data = lancam.descricao
            form.idLac.data = lancam.id
            return render_template('lancamentos/editLacmento.html', form=form, action='/lancamentos/lUpdate')

    today = date.today()
    #mantem a lista altualizada
    listTable = Lancamento.query.filter_by(users_id=current_user.id).\
        filter(extract('month', Lancamento.dtInic) == today.month).order_by(Lancamento.id.desc()).all()
    return render_template('lancamentos/lancamentos.html', form=form, listTable=listTable)

@lancamentos.route('/lancamentos/lUpdate', methods=['GET', 'POST'])
@login_required
def lUpdate():
    form = lancamentoForm(request.form)  # type: lancamentoForm
    if request.method == 'POST' and form.salvar.data == True:
        dateInic = datetime(form.dtInicio.data.year, form.dtInicio.data.month, form.dtInicio.data.day, 
            form.hrInicio.data.hour, form.hrInicio.data.minute, form.hrInicio.data.second)
        print(dateInic)

        dateEnd = datetime(form.dtFim.data.year, form.dtFim.data.month, form.dtFim.data.day, 
            form.hrFim.data.hour, form.hrFim.data.minute, form.hrFim.data.second)
        print(dateEnd)

        if form.validacao(form):
            flash('Falta preenchar um campo!', 'danger')
        elif form.valdDate(dateInic, dateEnd):
            flash('Data ou hora invalida!', 'danger')
        else:
            print(form.idLac.data)
            lancamento = Lancamento.query.filter_by(id=form.idLac.data).first_or_404()
            if lancamento:
                lancamento.project_id = form.selectProjeto.data
                lancamento.dtInic = dateInic.date()
                lancamento.hrInic = dateInic.time()
                lancamento.dtFim = dateEnd.date()
                lancamento.hrFim = dateEnd.time()
                lancamento.task_id = form.selectAtividade.data
                lancamento.descricao = form.descricao.data
                try:
                    db.session.commit()
                    flash('Registro alterado com sucesso', 'info')
                except:
                    db.session.rollback()
                    flash('Registro falhou em alterar', 'danger')
    return redirect(url_for('.lancamento'))