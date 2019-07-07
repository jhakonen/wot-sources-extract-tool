# Usage:
#  docker build --platform linux -t jhakonen/wot-sources .
#  docker run --rm -it -v c:/Games/World_of_Tanks:/input -v c:/tmp/output:/output jhakonen/wot-sources
FROM centos:7

# Install rpm packages
RUN yum -y update && yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install \
    python-pip \
    unzip \
    nano \
    python-pip \
    htop \
    iotop \
    wget \
    bsdtar \
    && \
    yum clean all

# Install pip packages
RUN pip install --upgrade pip && \
    pip install uncompyle6==2.12.0

# Install Java
RUN mkdir -p /opt/oracle && \
    (wget http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz \
        --header="Cookie:' gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie'" \
        -qO- | tar -xzv -C /opt/oracle)
RUN alternatives --install /usr/bin/java java /opt/oracle/jdk1.8.0_131/bin/java 2000 && \
    alternatives --install /usr/bin/jar jar /opt/oracle/jdk1.8.0_131/bin/jar 2 && \
    alternatives --install /usr/bin/javac javac /opt/oracle/jdk1.8.0_131/bin/javac 2 && \
    alternatives --set jar /opt/oracle/jdk1.8.0_131/bin/jar && \
    alternatives --set javac /opt/oracle/jdk1.8.0_131/bin/javac && \
    touch /etc/profile.d/oracle_jdk.sh && \
    echo "#!/bin/bash" >> /etc/profile.d/oracle_jdk.sh && \
    echo "export JDK_HOME=/opt/oracle/jdk1.8.0_131" >> /etc/profile.d/oracle_jdk.sh && \
    echo "export JAVA_HOME=/opt/oracle/jdk1.8.0_131" >> /etc/profile.d/oracle_jdk.sh && \
    echo "export JRE_HOME=/opt/oracle/jdk1.8.0_131/jre" >> /etc/profile.d/oracle_jdk.sh && \
    echo "export PATH=$PATH:/opt/oracle/jdk1.8.0_131/bin:/opt/oracle/jdk1.8.0_131/jre/bin" >> /etc/profile.d/oracle_jdk.sh && \
    chmod 555 /etc/profile.d/oracle_jdk.sh

# Install JPEXS Free Flash Decompiler
RUN mkdir -p /opt/ffdec && \
    wget https://github.com/jindrapetrik/jpexs-decompiler/releases/download/version10.0.0/ffdec_10.0.0.zip \
    -qO- | bsdtar -xvf- -C /opt/ffdec && \
    touch /usr/bin/ffdec && \
    echo "#!/bin/bash" >> /usr/bin/ffdec && \
    echo "java -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx1024m -jar /opt/ffdec/ffdec.jar \"\$@\"" >> /usr/bin/ffdec && \
    chmod 755 /usr/bin/ffdec

# Install decompiler
COPY entrypoint /entrypoint
RUN chmod 755 /entrypoint
COPY decompile /decompile
RUN chmod 755 /decompile
COPY wotsources/ /usr/lib/python2.7/site-packages/wotsources/
ENV PYTHONUNBUFFERED=1

VOLUME ["/input"]
VOLUME ["/output"]
ENTRYPOINT ["/entrypoint"]
CMD ["/decompile"]
