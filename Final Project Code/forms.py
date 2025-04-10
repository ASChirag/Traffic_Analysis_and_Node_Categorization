from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FloatField, FileField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class FileUploadForm(FlaskForm):
    file = FileField('Upload Data File', validators=[Optional(), FileAllowed(['csv', 'txt', 'json', 'pcap'], 'Only CSV, TXT, JSON, or PCAP files allowed!')])
    submit = SubmitField('Upload')

class TrafficAnalysisForm(FlaskForm):
    packet_size = FloatField('Packet Size (bytes)', validators=[Optional(), NumberRange(min=0)])
    connection_duration = FloatField('Connection Duration (seconds)', validators=[Optional(), NumberRange(min=0)])
    src_bytes = FloatField('Source Bytes', validators=[Optional(), NumberRange(min=0)])
    protocol = SelectField('Protocol', choices=[
        ('', 'Select Protocol'),
        ('tcp', 'TCP'),
        ('udp', 'UDP'),
        ('icmp', 'ICMP'),
        ('Unknown', 'Unknown')
    ], validators=[Optional()])
    submit = SubmitField('Analyze Traffic')

class NodeCategorizeForm(FlaskForm):
    ip_range = StringField('IP Address Range', validators=[Optional()])
    protocol = SelectField('Protocol Type', choices=[
        ('', 'Select Protocol'),
        ('tcp', 'TCP'),
        ('udp', 'UDP'),
        ('mqtt', 'MQTT'),
        ('icmp', 'ICMP')
    ], validators=[Optional()])
    packets_sent = FloatField('Packets Sent', validators=[Optional(), NumberRange(min=0)])
    device_type = SelectField('Device Type', choices=[
        ('', 'Select Device Type'),
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('server', 'Server'),
        ('workstation', 'Workstation'),
        ('iot', 'IoT Device')
    ], validators=[Optional()])
    traffic_volume = FloatField('Traffic Volume', validators=[Optional(), NumberRange(min=0)])
    connection_frequency = FloatField('Connection Frequency', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Categorize Node')

class AnomalyDetectionForm(FlaskForm):
    packets_sent = FloatField('Packets Sent', validators=[Optional(), NumberRange(min=0)])
    traffic_volume = FloatField('Traffic Volume', validators=[Optional(), NumberRange(min=0)])
    connection_duration = FloatField('Connection Duration (seconds)', validators=[Optional(), NumberRange(min=0)])
    connection_frequency = FloatField('Connection Frequency', validators=[Optional(), NumberRange(min=0)])
    protocol = SelectField('Protocol Type', choices=[
        ('', 'Select Protocol'),
        ('tcp', 'TCP'),
        ('udp', 'UDP'),
        ('icmp', 'ICMP'),
        ('mqtt', 'MQTT')
    ], validators=[Optional()])
    src_bytes = FloatField('Source Bytes', validators=[Optional(), NumberRange(min=0)])
    packet_size = FloatField('Packet Size (bytes)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Detect Anomalies') 