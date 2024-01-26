from celery import shared_task
from flask_mail import Message
from flask import render_template 
from uuid import uuid4
from datetime import datetime
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from celery import group,chain
from random import sample
from os.path import join
import numpy as np
import matplotlib
import pdfkit

@shared_task(name='celery.send_email_notification')
def send_email_notification(id):
    from . import User,mail,product,Product
    from .configuration import root_path
    user_data=User.query.filter_by(id=id).first()
    msg=Message()
    products=Product.query.all()
    if(not len(products)>3):
        return f"mail could not be sent because of not enough products available"
    sample_products=sample(products,3)
    for product_data in sample_products:
        image_name=product_data.product_image
        image_path=join(root_path,'product/static',image_name)
        with product.open_resource(image_path,'rb') as product_image:
            msg.attach(image_name,'image/*',product_image.read(),headers=[('Content-ID',f"{image_name}")])
    msg.recipients=[user_data.email]
    msg.subject="We've Missed You at Paper Basket"
    msg.html=render_template('customer_reminder.html',user=user_data,products=sample_products)
    mail.send(msg)
    return f"mail sent to {user_data.email}"

@shared_task(name='celery.send_reset_password')
def send_reset_password(id,token,hostname,port):
    from . import User,mail
    user=User.query.get(id)
    msg=Message()
    msg.recipients=[user.email]
    msg.subject="Reset password of your Paper Basket account"
    msg.html=render_template('reset_password.html',user=user,token=token,hostname=hostname,port=port)
    mail.send(msg)
    return f"mail with reset link sent to {user.email}"

@shared_task(name='celery.send_confirmation')
def send_confirmation(id,token,hostname,port):
    from . import User,mail
    user=User.query.get(id)
    msg=Message()
    msg.recipients=[user.email]
    if 'Customer' in user.roles:
        msg.subject="Activate Your Paper Basket Account"
        msg.html=render_template('customer_verification.html',user=user,token=token,hostname=hostname,port=port)
    if 'Manager' in user.roles:
        msg.subject="Store Manager Application Approved"
        msg.html=render_template('manager_verification.html',user=user,token=token,hostname=hostname,port=port)
    mail.send(msg)
    return f"confirmation mail sent to {user.email}"

@shared_task(name='celery.manager_confirmation')
def manager_confirmation(id,token):
    from . import User,mail
    user=User.query.get(id)
    msg=Message()
    msg.recipients=[user.email]
    msg.subject="Activate Your Paper Basket Account"
    msg.html=render_template('customer_verification.html',user=user,token=token)
    mail.send(msg)
    return f"confirmation mail sent to {user.email}"

@shared_task(name='celery.customer_daily_inform')
def customer_daily_inform():
    from . import User,Role
    today=datetime.date(datetime.today())
    role=Role.query.filter_by(name='Customer').first()
    users=User.query.filter(User.roles.contains(role)).all()
    tasks=[send_email_notification.s(user.id) for user in users if today>user.signin_date or True]
    group(tasks).delay()

@shared_task(name='celery.send_email_monthly_report')
def send_email_monthly_report(result,user_id):
    from . import mail,User
    filename,pdf_content,orders,total_amount,month,year=result
    user=User.query.filter_by(id=user_id).first()
    content={'user':user,'orders':orders,'total_amount':round(total_amount,2),
             'month':month,'year':year}
    msg=Message()
    msg.recipients=[user.email]
    msg.subject="Your Monthly Shopping Summary with Paper Basket"
    msg.html=render_template('customer_monthly_report.html',**content)
    msg.attach(filename,'application/pdf',pdf_content)
    mail.send(msg)
    return f"mail sent to {user.email}"

@shared_task(name='celery.generate_pdf_report')
def generate_pdf_report(user_id):
    from jinja2 import Environment,FileSystemLoader
    from application.configuration import root_path
    from . import User,Order,Product
    from os import path
    previous_date=datetime.date(datetime.today())-relativedelta(months=1)
    present_date=datetime.date(datetime.today())
    month=previous_date.strftime('%B')
    year=previous_date.strftime('%Y')
    current_user=User.query.filter_by(id=user_id).first()
    orders=Order.query.filter_by(user=current_user).all()
    products=Product.query.all()
    current_user_orders=[]
    total_amount=0
    for product in products:
        qty_purchased,price_spend=0,0
        for order in orders:
            if (previous_date<=order.order_date<present_date):
                if (product.name==order.name):
                    total_amount+=order.price
                    qty_purchased+=order.quantity
                    price_spend+=order.price
        if qty_purchased>0:
            current_user_orders.append({ 'name': product.name,
                                         'supplier': product.supplier,
                                         'category': product.category.name,
                                         'quantity': qty_purchased,
                                         'unit': product.unit,
                                         'price': round(price_spend,2) })
    template_path=path.join(path.abspath(root_path),'application','templates')
    env=Environment(loader=FileSystemLoader(template_path))
    template=env.get_template('customer_report_pdf.html')
    content={'user':current_user,'orders':current_user_orders,'total_amount':round(total_amount,2),'month':month,'year':year}
    pdf_data=template.render(**content)
    filename=f'{current_user.first_name}_{current_user.last_name}_{month}_{year}.pdf'
    pdf_content=pdfkit.from_string(pdf_data,False,options={'encoding': 'UTF-8'})
    return [filename,pdf_content,current_user_orders,total_amount,month,year]

@shared_task(name='celery.customer_monthly_report')
def customer_monthly_report():
    from . import User,Role
    role=Role.query.filter_by(name='Customer').first()
    users=User.query.filter(User.roles.contains(role)).all()
    tasks=[chain(generate_pdf_report.s(user.id),send_email_monthly_report.s(user.id)) for user in users]
    group(tasks).delay()

@shared_task(name='celery.generate_graphs')
def generate_graphs(category,data):
    matplotlib.use('agg')
    X=np.array(list(filter(lambda x:x[1]==category,data)))
    months_no=np.arange(0,14)
    month_names = ["","Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",""]
    if(X.size!=0):
        products=set(X[:,0])
        for current_product in products:
            x_pts,y_pts,month=[],[],0
            for y in range(1,13):
                qty=0
                month=y
                for x in X:
                    current_month=int(x[2])
                    if current_product==x[0] and current_month==y:
                        qty+=int(x[3])
                if qty!=0:
                    x_pts.append(month)
                    y_pts.append(qty)
            plt.scatter(x_pts,y_pts,label=current_product)
        plt.ylim(0,max(y_pts)+5)
    else:
        plt.ylim(0,5)
    plt.legend(title="Products")
    plt.xlabel('Month')
    plt.ylabel('Quantity')
    plt.xticks(months_no,month_names)
    plt.title(f'{category}: Quantity vs Month')
    plt.savefig(fname=f'./application/static/{category.lower()}.svg',format='svg')
    plt.clf()
    return f"graph generated for {category}"

@shared_task(name='celery.generate_csv')
def generate_csv(data):
    dataset=np.array(data)
    filename=f'{uuid4()}.csv'
    np.savetxt(fname=f'./temp/{filename}',X=dataset,delimiter=',',fmt='%s',
               header="Product Name,Category Name,Unit,Quantity Sold,Total Sold Price,Quantity Remain,Total Remain Price")
    return filename

    
        
