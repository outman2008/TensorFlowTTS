#!/usr/bin/env python
# coding: utf-8
# 调用方式
# python online_tts.py -client_secret=你的client_secret -client_id=你的client_secret -file_save_path=test.wav --text=今天天气不错哦 --audiotype=6
from typing import TextIO

import requests
import json
import argparse
import os
import time
from g2p_en import G2p as grapheme_to_phn
import random
import soundfile as sf
import winsound


# 获取access_token用于鉴权
def get_access_token(client_secret, client_id):
    grant_type = "client_credentials"
    url = "https://openapi.data-baker.com/oauth/2.0/token?grant_type={}&client_secret={}&client_id={}".format(
        grant_type, client_secret, client_id)
    response = requests.post(url)
    print("requests", url, response.text)
    access_token = json.loads(response.text).get('access_token')
    print("access_token", access_token)
    return access_token


# 获取转换后音频
def get_audio(data):
    url = "https://openapi.data-baker.com/tts?access_token={}&domain={}&language={}&voice_name={}&text={}&audiotype={}".format(
        data['access_domain'], data['domain'], data['language'], data['voice_name'], data['text'], data['audiotype'])
    response = requests.post(url)
    # print("get_audio", url, response.text)
    content_type = response.headers['Content-Type']
    if 'audio' not in content_type:
        raise Exception(response.text)
    return response.content


# 获取命令行输入参数
def get_args():
    text = '欢迎使用标贝开发平台。'
    parser = argparse.ArgumentParser(description='TTS')
    parser.add_argument('-client_secret', type=str, default='6e79b28ab1554830abaf797b10de0432')
    parser.add_argument('-client_id', type=str, default='84f3dba6a69b42078f9fe1942ba8ecf3')
    parser.add_argument('-file_save_path', type=str)
    parser.add_argument('--text', type=str, default=text)
    parser.add_argument('--audiotype', type=str, default='6')
    parser.add_argument('--domain', type=str, default='1')
    parser.add_argument('--language', type=str, default='zh')
    parser.add_argument('--voice_name', type=str, default='Jiaojiao')
    args = parser.parse_args()

    return args


train_f_name: str = "metadata.csv"
data_dir: str = "C:\\Users\\outman.t.yang\\Pictures\\baker_test\\new"
positions = {
    "wave_file": 0,
    "text": 1,
    "text_norm": 2,
}

get_g2p = grapheme_to_phn()


def create_items():
    with open(
            os.path.join(data_dir, train_f_name), encoding="utf-8"
    ) as ttf:
        # [split_line(data_dir, line, "|") for line in f.readlines()
        lines = ttf.readlines()
        for idx in range(0, len(lines), 1):
            line = lines[idx].strip()
            if idx < 1000:
                continue
            if idx > 1500:
                break
            print('create idx', idx)
            split_line(line, '|')


# def create_wavs(access_token, args):
#     file_list = os.listdir(data_dir)
#     for file in file_list:
#         fileName = os.path.splitext(file)
#         if fileName[1] == '.txt':
#             file_path = os.path.join(data_dir, file)
#             # with open(file_path, encoding="utf-8") as ttf:
#             #     line = ttf.readline().strip()
#             utt_id = fileName[0]
#             wav_path = os.path.join(data_dir, "%s.wav" % utt_id)
#             utt_id = utt_id.replace("LJ00", "2")
#             utt_id = utt_id.replace("-", "")
#             dstTxt = os.path.join(data_dir, "%s.txt" % utt_id)
#             dstWav = os.path.join(data_dir, "%s.wav" % utt_id)
#             os.rename(file_path, dstTxt)
#             os.rename(wav_path, dstWav)
#             print('create_items rename', utt_id)
#             # # 读取参数
#             # audiotype = args.audiotype
#             # domain = args.domain
#             # language = args.language
#             # voice_name = args.voice_name
#             # data = {'access_domain': access_token, 'audiotype': audiotype, 'domain': domain, 'language': language,
#             #         'voice_name': voice_name, 'text': line}
#             # content = get_audio(data)
#             # # 保存音频文件
#             # with open(wav_path, 'wb') as audio:
#             #     audio.write(content)
#             # time.sleep(0.1)
#             # print('create_items', utt_id)
charList = []


def create_char_list(len, max):
    for num in range(1, max):
        str = chr(random.randint(97, 122))
        for i in range(1, len):
            str += ',' + chr(random.randint(97, 122))
        str = str.upper()
        if str not in charList:
            charList.append(str)
        else:
            print('charList in', str)


def create_wavs(access_token, args):
    for num in range(97, 123):
        charList.append(chr(num).upper())

    # 5个字母的200个
    create_char_list(5, 200)
    # 8个字母的150个
    create_char_list(8, 150)
    # 10个字母的150个
    create_char_list(10, 150)
    i = 200000
    for charStr in charList:
        i += 1
        print('charStr', i, charStr)
        txt_path = os.path.join(data_dir, "%s.txt" % i)
        if not os.path.exists(txt_path):
            fo = open(txt_path, "w")
            fo.write(charStr)
            # 关闭文件
            fo.close()
        # 读取参数
        audiotype = args.audiotype
        domain = args.domain
        language = args.language
        voice_name = args.voice_name
        data = {'access_domain': access_token, 'audiotype': audiotype, 'domain': domain, 'language': language,
                'voice_name': voice_name, 'text': charStr}
        content = get_audio(data)
        # 200000 + num
        wav_path = os.path.join(data_dir, "%s.wav" % i)
        # 保存音频文件
        with open(wav_path, 'wb') as audio:
            audio.write(content)
        time.sleep(0.1)


def get_phoneme_from_g2p_en(en_char):
    parts = en_char.split(' ')
    result = ["sil"]
    for word in parts:
        word = word.strip()
        if len(word) > 0:
            phn_arr = get_g2p(word)
            print('phn_arr', phn_arr)
            phn_arr = [x for x in phn_arr if (x != " " and x != "." and x != ",")]
            result += phn_arr
            result.append("#0")
    if result[-1] == "#0":
        result = result[:-1]
    result.append("sil")
    text = " ".join(result)
    return text


def split_line(line, split):
    parts = line.strip().split(split)
    wave_file = parts[positions["wave_file"]]
    text_norm = parts[positions["text_norm"]]
    wav_path = os.path.join(data_dir, "wavs", f"{wave_file}.wav")
    if os.path.exists(wav_path):
        fPath = os.path.join(data_dir, f"{wave_file}.txt")
        if not os.path.exists(fPath):
            print('split_line', fPath)
            fo = open(fPath, "w")
            fo.write(text_norm)
            # 关闭文件
            fo.close()


if __name__ == '__main__':
    try:
        # args = get_args()
        # # create_items()
        # # 获取access_token
        # # client_secret = args.client_secret
        # # client_id = args.client_id
        # # # print("running", args)
        # # access_token = get_access_token(client_secret, client_id)
        # # print("access_token", access_token)
        # access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiKiJdLCJzY29wZSI6WyJ0dHMtb25lc2hvdCJdLCJleHAiOjE2Mzk0NjQwMzMsImF1dGhvcml0aWVzIjpbIioiXSwianRpIjoiNjk2MTM0NGItODMyZS00YWJkLTllNDgtMDVjOWJlNDU4YTRhIiwiY2xpZW50X2lkIjoiODRmM2RiYTZhNjliNDIwNzhmOWZlMTk0MmJhOGVjZjMifQ.uwdrR7TjZZjyO3VAb2FN4v_MJz8vCjcriIA3yLSGTHc'
        # # # 读取参数
        # audiotype = args.audiotype
        # domain = args.domain
        # language = args.language
        # voice_name = args.voice_name
        # create_wavs(access_token, args)
        # text = args.text
        # data = {'access_domain': access_token, 'audiotype': audiotype, 'domain': domain, 'language': language,
        #         'voice_name': voice_name, 'text': text}
        # content = get_audio(data)

        # # 保存音频文件
        # with open('test.wav', 'wb') as audio:
        #     audio.write(content)
        # txt = get_phoneme_from_g2p_en("All prisoners passed their time in absolute idleness, or killed it by gambling and loose conversation.")
        # print(txt)
        audio_lst = ['200003', '200006', '200008']
        audios = []
        for word in audio_lst:
            wav_path = os.path.join(data_dir, f"{word}.wav")
            print(wav_path)
            if os.path.exists(wav_path):
                # with open(wav_path, 'rb') as audio:
                audio, rate = sf.read(wav_path)
                print(audio)
                # winsound.PlaySound(audio.read(), winsound.SND_MEMORY)
                audios.append(audio)
        # winsound.PlaySound(audios, winsound.SND_MEMORY)
    except Exception as e:
        print(e)
