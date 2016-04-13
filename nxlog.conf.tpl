########
$NXLOG_CONFIG_DIR = /etc/nxlog
#$CERTDIR
#$MODULSDIR
#$LOG_NAME
#$LOG_PATH
#$HOSTNAME
#$Tag
########
define ROOT  {{ NXLOG_CONFIG_DIR }}
#/root/nxlog_workpace
define CERTDIR {{ CERTDIR }}
#/root/nxlog_workpace/ssl

Moduledir /usr/lib/nxlog/modules/
#/usr/lib/nxlog/modules

CacheDir %ROOT%/data

Pidfile %ROOT%/data/nxlog.pid

SpoolDir %ROOT%/data

LogFile %ROOT%/data/nxlog.log

<Processor evcorr>
    Module        pm_evcorr
    <Simple>
        Exec $raw_event = "FILE="+$FileName+" "+"HOST="+$HostName+" "+"KEY="+$StreamKey+" "+"TYPE="+$StreamType+" "+"TAG="+$StreamTag+" "+$raw_event;
    </Simple>
</Processor>

{% set a = var_dict %}
<Input in>
    Module       {{ a.LOG_NAME }}
    File         {{ a.LOG_PATH }}
    SavePos        TRUE
    PollInterval 1
    # Explicitly set the Hostname. This defaults to the system's hostname if unset.
    Exec    $HostName = {{ HOSTNAME }};
    Exec    $StreamKey = {{ STREAMKEY }};
    Exec    $StreamType = {{ SREAMTYPE }};
    Exec    $StreamTag = {{ STREAMRAG }} ;

    Exec    $FileName = file_name();
</Input>



<Input tcp_in>
    Module	im_tcp
    Port	12000
    Host	127.0.0.1
</Input>

<Output tcp_out>
    Module	om_file
    File	"tcp_test.log"
</Output>

<Output sslout>
    Module	om_ssl
    Host	127.0.0.1
    Port	12000
    CAFile	%CERTDIR%/ca.crt
    CertFile	%CERTDIR%/server.crt
    CertKeyFile %CERTDIR%/server.key
    KeyPass	123456
    AllowUntrusted  TRUE
    OutputType	Binary
</Output>

<Output out>
    Module        om_tcp
    Host        127.0.0.1
    Port        12000
</Output>

<Route 1>
    Path        in => evcorr => sslout
</Route>

