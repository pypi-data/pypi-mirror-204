import json
import sys
from urllib import response
sys.path.append(".")
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch
from myapp.models import Book
from django.http import JsonResponse
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from rest_framework.views import APIView

def send_email(request,email):
        if request.method == 'GET':
            print('succ')
            books = Book.objects.filter(email=email, status= 'BOOKED').last()
            try:
                cost = int(books.nos) * int(books.price)
                buffer = BytesIO()
                p = canvas.Canvas(buffer, pagesize=letter)
                # Define the header
                p.setLineWidth(.3)
                p.setFont('Helvetica', 22)
                p.drawString(30, 750, 'Blue Bus: Ticket Confirmation')
                p.setFont('Helvetica', 12)
                p.drawString(30, 735, 'Please find below booking information')

                # Define the footer
                p.setFont('Helvetica', 12)
                p.drawString(5.5 * inch, 0.75 * inch, "www.bluebus.com")

                
                data = [    ["Name", books.name],
                            ["Bus Name", books.bus_name],
                            ["Starting Point", books.source],
                            ["Destination Point", books.dest],
                            ["Number of Seats", books.nos],
                            ["Price", books.price],
                            ["Cost", cost],
                            ["Date", books.date],
                            ["Time", books.time],
                            ["Booking Status", books.status],
                        ]
                # Define table style
                style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),    
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),    
                                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),    
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    
                                    ('FONTSIZE', (0, 0), (-1, 0), 14),    
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),    
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),    
                                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),    
                                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),    
                                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),    
                                    ('FONTSIZE', (0, 1), (-1, -1), 12),    
                                    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),    
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black),])
                                    

                # Create table object and apply style
                table = Table(data)
                table.setStyle(style)

                # Add table to PDF
                table.wrapOn(p, 0, 0)
                table.drawOn(p, 100, 450)

                # Save PDF
                p.showPage()
                p.save()
                pdf = buffer.getvalue()
                buffer.close()

                subject = 'Bus Ticket Confirmation'
                txt_ = 'Please find attached your bus ticket confirmation.'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [books.email]
                html_ = request.GET.get('html')
                email = EmailMessage(subject=subject,body=txt_,from_email=from_email,to=recipient_list)
                email.attach('bus_ticket.pdf', pdf, 'application/pdf')
                email.send(fail_silently=False)
            except Exception as e:
                print('error')
                print(e)
                return JsonResponse({'msg': 'fail'})
        return JsonResponse({'msg': 'success'})



