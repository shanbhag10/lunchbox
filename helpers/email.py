import boto3
from botocore.exceptions import ClientError


def build_order_ready_email(order, user, chef):
	html_body = """
	<html>
	<head>
	<style>
		.order_items,
		table.order_items td, 
		table.order_items tr, 
		table.order_items th {
			border-collapse: collapse;
			border: 1px solid black;
			text-align: center;
			padding: 5px;
		}
	</style>
	</head>
	<body>
	  <h1>Order #"""
	  
	html_body += str(order.id) +	" is ready</h1>"
	html_body += "<p>Hi " + user.first_name + ", "

	gmaps_url = 'https://www.google.com/maps/dir//' + chef.address.replace(" ", "+")
	
	html_body += "<p>Please pick up your order from Chef " + chef.first_name + " at "
	html_body += "<a href='" + gmaps_url + "'>" + chef.address + ".</a></p>"

	html_body += "<h3>Order Details</h3>"
	html_body += """
		<table class="order_items">
		<tr>
            <th>Item Name</th>
            <th>Quantity</th>
        </tr>
	"""

	for order_item in order.order_items:
		html_body += "<tr>"
		html_body += "<td>" + order_item.item.name + "</td>"
		html_body += "<td>" + str(order_item.qty) + "</td>"
		html_body += "</tr>"

	html_body += "</table>"
	html_body += "<p><b>Total Cost: $</b>" + str(order.total_cost) +"</p>"
	html_body += "<h3>Enjoy!</h3>"		
	html_body += "</body></html>"

	return html_body


def send_email(email, subject, body):
	SENDER = "LunchBox Order <hello.lunchbox.app@gmail.com>"
	
	CHARSET = "UTF-8"
	
	client = boto3.client('ses',region_name="us-west-1")

	try:
	    response = client.send_email(
	        Destination={
	            'ToAddresses': [
	                email,
	            ],
	        },
	        Message={
	            'Body': {
	                'Html': {
	                    'Charset': CHARSET,
	                    'Data': body,
	                },
	                'Text': {
	                    'Charset': CHARSET,
	                    'Data': body,
	                },
	            },
	            'Subject': {
	                'Charset': CHARSET,
	                'Data': subject,
	            },
	        },
	        Source=SENDER,
	    )
	except ClientError as e:
	    print("Email sending failed: " + e.response['Error']['Message'])
	else:
	    print("Email sent! Message Id :" + response['MessageId'])