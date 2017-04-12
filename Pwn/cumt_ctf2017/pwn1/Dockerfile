FROM ubpwn16:base
MAINTAINER pwn1
LABEL Description="bxs pwn1" VERSION='1.0'

#user
RUN adduser --disabled-password --gecos '' bxs1
RUN chown -R root:bxs1 /home/bxs1/
RUN chmod 750 /home/bxs1
RUN touch /home/bxs1/flag.txt
RUN chown root:bxs1 /home/bxs1/flag.txt
RUN chmod 440 /home/bxs1/flag.txt
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/bxs1/
COPY bxs1 /home/bxs1
COPY flag.txt /home/bxs1

EXPOSE 22333
CMD su bxs1 -c "socat -T10 TCP-LISTEN:22333,reuseaddr,fork EXEC:/home/bxs1/bxs1"
