FROM ubpwn16:base
MAINTAINER pwn4
LABEL Description="bxs pwn4" VERSION='1.0'

#user
RUN adduser --disabled-password --gecos '' bxs4
RUN chown -R root:bxs4 /home/bxs4/
RUN chmod 750 /home/bxs4
RUN touch /home/bxs4/flag.txt
RUN chown root:bxs4 /home/bxs4/flag.txt
RUN chmod 440 /home/bxs4/flag.txt
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/bxs4/
COPY bxs4 /home/bxs4
COPY flag.txt /home/bxs4

EXPOSE 54321
CMD su bxs4 -c "socat -T10 TCP-LISTEN:54321,reuseaddr,fork EXEC:/home/bxs4/bxs4"
