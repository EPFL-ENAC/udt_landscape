FROM httpd:2.4

RUN apt-get -qy update \
    && apt-get -qy install wget sed

# Enable SSL
RUN sed -i \
    -e 's/^#\(Include .*httpd-ssl.conf\)/\1/' \
    -e 's/^#\(LoadModule .*mod_ssl.so\)/\1/' \
    -e 's/^#\(LoadModule .*mod_socache_shmcb.so\)/\1/' \
    conf/httpd.conf

# Install Apache OpenIDC
RUN cd / \
    && wget https://github.com/OpenIDC/mod_auth_openidc/releases/download/v2.4.16.8/libapache2-mod-auth-openidc_2.4.16.8-1.bookworm_amd64.deb \
    && apt-get -qy install ./libapache2-mod-auth-openidc_2.4.16.8-1.bookworm_amd64.deb

RUN mkdir /var/log/apache2/ \
    && chown www-data: /var/log/apache2/

# Enable proxy
COPY ./apache.conf /usr/local/apache2/conf/custom.conf
COPY ./oidc.secret.conf /usr/local/apache2/conf/oidc.secret.conf
RUN echo "\nInclude /usr/local/apache2/conf/custom.conf\n"\
    >> /usr/local/apache2/conf/httpd.conf

EXPOSE 80 443
