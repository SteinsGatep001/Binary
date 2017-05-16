#include <fcntl.h>
#include <iostream> 
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <stdio.h>

using namespace std;

#define GENDER_LENGTH 20
#define NAME_LENGTH 100
#define STORY_LENGTH 100
#define SKILL_LENGTH 100

void tb_system(char *buggg, char *lcmd)
{
    system(lcmd);
    system(buggg);
}

void mwrite_buf(char *buf)
{
    write(1, buf, strlen(buf));
}

int read_mbuf(char *buf, int length)
{
    char tmp_ch;
    int i;
    for(i=0; i<length; i++)
    {
        read(0, &tmp_ch, 1);
        if(tmp_ch == '\n')
            break;
        buf[i] = tmp_ch;
    }
    return i;
}

int get_int()
{
    int tmp;
    char tmp_buf[7];
    int length = read_mbuf(tmp_buf, 6);
    if(length<=0)
        return -1;
    return atoi(tmp_buf);
}

class TBCharacter
{
protected:
    int atk;
    int matk;
    char gender[GENDER_LENGTH];
    char *name;
    char *story;
public:
    TBCharacter(int atk, int matk, char *gender, char *name, char *story)
    {
        printf("init character\n");
        this->atk = atk;
        this->matk = matk;
        strcpy(this->gender, gender);
        this->name = new char[NAME_LENGTH];
        strcpy(this->name, name);
        this->story = new char[STORY_LENGTH];
        strcpy(this->story, story);
    }
    ~TBCharacter()
    {
        delete name;
        delete story;
    }
    virtual void info()
    {
        char buf_tmp[2048];
        int story_bytes = 0;
        sprintf(buf_tmp, "name:%s\nattack:%d\tmagic attack:%d\n", this->name, this->atk, this->matk);
        mwrite_buf(buf_tmp);
        mwrite_buf("how many story do you want to read?\n");
        story_bytes = get_int();
        write(1, this->story, story_bytes);
        mwrite_buf("\nGood story. Isnt it?\n");
    }
    virtual void set_info(char *story, int atk, int matk)
    {
        this->atk = atk;
        this->matk = matk;
        strcpy(this->story, story);
    }
};

class TBPhysical: public TBCharacter
{
    int phy_boost;
public:
    TBPhysical(int atk, int matk, char *gender, char *name, char *story) : TBCharacter(atk, matk, gender, name, story)
    {
        mwrite_buf("init physical character\n");
    }
    virtual void info()
    {
        char buf_tmp[100];
        TBCharacter::info();
        sprintf(buf_tmp, "physical attack boost: %d\n", this->phy_boost);
        mwrite_buf(buf_tmp);
        mwrite_buf("**********************Physical************************\n");
    }
    virtual void set_info(char *story, int atk, int matk)
    {
        TBCharacter::set_info(story, atk, matk);
    }
};

class TBMagic: public TBCharacter
{
    int mag_luck;
    char *skill_name;
public:
    TBMagic(int atk, int matk, char *gender, char *name, char *story, int mag_luck, char *skill_name) : TBCharacter(atk, matk, gender, name, story)
    {
        printf("init magic character\n");
        this->mag_luck = mag_luck;
        this->skill_name = new char[SKILL_LENGTH];
        strcpy(this->skill_name, skill_name);
    }
    ~TBMagic()
    {
        delete skill_name;
    }
    virtual void info()
    {
        char buf_tmp[100];
        TBCharacter::info();
        sprintf(buf_tmp, "magic lucky: %d\t skill name: %s\n", this->mag_luck, this->skill_name);
        mwrite_buf(buf_tmp);
        mwrite_buf("+++++++++++++++++++++++++++++++Magic+++++++++++++++++++++++++++++++++\n");
    }
    virtual void set_info(char *story, int atk, int matk)
    {
        TBCharacter::set_info(story, atk, matk);
    }
};

class GameControl
{
protected:
    int number_character;
public:
    GameControl()
    {
        mwrite_buf("===========================Terra Battle=====================================\n");
        mwrite_buf("welcome to terra battle game wiki center\n");
        mwrite_buf("while it is wiki, you can set some information of charcters\n");
        mwrite_buf("you can change physical, magic attack and story\n");
        mwrite_buf("===========================Terra Battle=====================================\n");
    }
    ~GameControl()
    {
        mwrite_buf("Game over\n");
    }

    void print_menu()
    {
        mwrite_buf("1: list character info\n");
        mwrite_buf("2: change character info\n");
        mwrite_buf("3: delete character\n");
        mwrite_buf("4: create your story\n");
        mwrite_buf("===========================Terra Battle=====================================\n");
    }

    void change_chrinfo(TBCharacter* optCharacter)
    {
        char *tmp_story;
        int tmp_atk, tmp_matk;
        mwrite_buf("atk: ");
        tmp_atk = get_int();
        mwrite_buf("matk: ");
        tmp_matk = get_int();
        mwrite_buf("story: ");
        tmp_story = new char[STORY_LENGTH];
        read_mbuf(tmp_story, STORY_LENGTH);
        optCharacter->set_info(tmp_story, tmp_atk, tmp_matk);
        delete tmp_story;
    }
};


int main()
{
    int moption, opt_which;
    GameControl* gameControl = new GameControl();
    TBCharacter* yukken = new TBPhysical(441, 321, "Female", "Yukken", "Yukken loves book");
    TBCharacter* bahl = new TBPhysical(418, 264, "Female", "Bahl", "The master of sword");
    TBCharacter* mizell = new TBMagic(327, 618, "Female", "Mizell", "Shy at heart, she hates confrontation and lives her life as unobtrusively as possiable", 100, "X-Treme,Princer Area");
    char* you_story = NULL;
    int tmp_length;
    TBCharacter* tmpCharacter;
    while(1)
    {
        mwrite_buf("what waifu do you want to?(other number to pass this)\n");
        mwrite_buf("1. Yukken\n");
        mwrite_buf("2. Bahl\n");
        mwrite_buf("3. Mizell\n");
        mwrite_buf("===========================Terra Battle=====================================\n");
        opt_which = get_int();
        switch(opt_which)
        {
            case 1:
                tmpCharacter = yukken;
                break;
            case 2:
                tmpCharacter = bahl;
                break;
            case 3:
                tmpCharacter = mizell;
                break;
            default:
                tmpCharacter = 0;
                mwrite_buf("okok\n\n");
                break;
        }
        gameControl->print_menu();
        moption = get_int();
        switch(moption)
        {
            case 1:
                if(tmpCharacter != NULL)
                    tmpCharacter->info();
                break;
            case 2:
                if(tmpCharacter != NULL)
                    gameControl->change_chrinfo(tmpCharacter);
                break;
            case 3:
                if(tmpCharacter != NULL)
                    delete tmpCharacter;
                break;
            case 4:
                mwrite_buf("how long of your story?\n");
                tmp_length = get_int();
                you_story = new char[tmp_length];
                mwrite_buf("tell your story23333\n");
                read_mbuf(you_story, tmp_length);
                break;
            default:
                mwrite_buf("no such choice\n");
                break;
        }
    }
    return 0;
}


