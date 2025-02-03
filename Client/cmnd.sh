google-chrome --user-data-dir=/tmp/chrome-profile --no-proxy-server --enable-quic --origin-to-force-quic-on=www.example.org:443 --host-resolver-rules='MAP www.example.org:443 192.168.192.235:6121' https://www.example.org/index_5KB.html -–disable_certificate_verification

