import argparse
import json
from scraper import hacker_scrape
from flask import Flask



def hacker_cli():
    parser = argparse.ArgumentParser(description="gets certain number of results from hacker-news.json")
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), help='importing json file')
    parser.add_argument('-s', '--search', type=int, action='store', help='searches json file by rank number')
    args = parser.parse_args()
    
    if args.input:
        data = json.load(args.input)
        for rows in data:
            print(rows)
            
    if args.search and args.input:
        try:
            res = json.load(args.input)
            for rows in res:
                print(rows)
        except Exception as e:
            raise e
        results = []
        for ranks in res:
            if args.search in ranks["rank"]:
                results.append(ranks)
            print(f'{len(results)} results were found!')
            for rank_num in results:
                print(rank_num)
                pass
                
if __name__ == '__main__':
    print(hacker_cli())    