from __future__ import annotations

import json
import re


class DFSJson:
    def __init__(self, max_depth=100, max_diff=5):
        self.max_depth = max_depth
        self.max_diff = max_diff
        self.search_pattern = r'([\[\]\(\)\{\}\,\"\'])'
        self.replace_characters = """\"\',+ }{()]"""
        return

    @staticmethod
    def dump(*args):
        return json.dump(*args)

    @staticmethod
    def dumps(*args):
        return json.dumps(*args)

    def load(self, f):
        string = f.read()
        return self.loads(string)

    def loads(self, string):
        try:
            return json.loads(string)
        except json.JSONDecodeError:
            # most basic error is using ' instead of "
            string = string.replace("'", '"')
            fixed_json, fitness = self.dfs(string, self.max_depth)
            return json.loads(fixed_json)

    @staticmethod
    def fitness(string):
        try:
            json.loads(string)
            return int(1e8)  # No error
        except json.JSONDecodeError as e:
            return e.pos

    @staticmethod
    def mutate(string, index, replacement, flag='insert'):
        if flag == 'insert':
            # insert character
            return string[:index] + replacement + string[index:]
        elif flag == 'replace':
            # replace character
            return string[:index] + replacement + string[index + 1:]
        else:
            return ValueError

    @staticmethod
    def level_diff(string):
        diff1 = abs(
            len(re.findall(r'{', string)) - len(re.findall(r'}', string)),
        )
        diff2 = abs(
            len(re.findall(r'\[', string)) - len(re.findall(r'\]', string)),
        )
        return max(diff1, diff2)

    def dfs(self, string, max_depth=10, cur_fitness=None, visited=None):
        if visited is None:
            visited = set()
        if cur_fitness is None:
            cur_fitness = self.fitness(string)
        if max_depth < 0:
            return string, 0
        if cur_fitness == int(1e8):
            return string, cur_fitness
        best_fitness = cur_fitness
        best_string = string
        indexes = [cur_fitness] + [
            r.span()[0]
            for r in re.finditer(self.search_pattern, string)
        ]
        diff = -self.max_diff

        for index in indexes:
            for m in self.replace_characters:
                for mutate_type in ['insert', 'replace']:
                    new_string = self.mutate(string, index, m, mutate_type)
                    diff = self.level_diff(new_string)
                    if diff > self.max_diff:
                        continue
                    if new_string in visited:
                        continue
                    new_fitness = self.fitness(new_string)
                    if new_fitness > best_fitness + 1:
                        best_fitness = new_fitness
                        best_string = new_string
                        if best_fitness == int(1e8) and diff == 0:
                            break

        if best_fitness < int(1e8) and diff != 0:
            return self.dfs(
                best_string,
                max_depth - 1,
                best_fitness,
                visited.copy().union({best_string}),
            )
        else:
            return best_string, best_fitness
