FROM ubpwn16:base
MAINTAINER pwn2
LABEL Description="bxs pwn2" VERSION='1.0'

#install 32bit lib
RUN apt-get install -y lib32z1 lib32ncurses5 lib32stdc++6

#user
RUN adduser --disabled-password --gecos '' bxs2
RUN chown -R root:bxs2 /home/bxs2/
RUN chmod 750 /home/bxs2
RUN touch /home/bxs2/flag.txt
RUN chown root:bxs2 /home/bxs2/flag.txt
RUN chmod 440 /home/bxs2/flag.txt
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/bxs2/
COPY bxs2 /home/bxs2
COPY flag.txt /home/bxs2

EXPOSE 24500
CMD su bxs2 -c "socat -T10 TCP-LISTEN:24500,reuseaddr,fork EXEC:/home/bxs2/bxs2"
