FROM ubpwn16:base
MAINTAINER pwn3
LABEL Description="bxs pwn3" VERSION='1.0'

#user
RUN adduser --disabled-password --gecos '' bxs3
RUN chown -R root:bxs3 /home/bxs3/
RUN chmod 750 /home/bxs3
RUN touch /home/bxs3/flag.txt
RUN chown root:bxs3 /home/bxs3/flag.txt
RUN chmod 440 /home/bxs3/flag.txt
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/bxs3/
COPY bxs3 /home/bxs3
COPY flag.txt /home/bxs3

EXPOSE 22666
CMD su bxs3 -c "socat -T10 TCP-LISTEN:22666,reuseaddr,fork EXEC:/home/bxs3/bxs3"
