import os
import javalang

class Parse:
    def __init__(self, name, source_code):
        self.name = name
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.tree = javalang.parse.parse(self.source_code)
        
        self.end_line = self.FindClassEndLine()
        self.return_lines = self.FindClassReturnLine()
        self.isValid = True
        if self.end_line == None:
            self.isValid = False
        else:
            self.methods = self.FindMethodRange()            
            self.fine_blocks, self.coarse_blocks = self.ParseCodeBlocks()

    def FindClassReturnLine(self):
        return_lines = []
        for path, node in self.tree:
            if isinstance(node, javalang.tree.ReturnStatement):
                return_lines.append(node.position.line)
        return return_lines


    def FindClassEndLine(self):
        for path, node in self.tree:
            if isinstance(node, javalang.tree.ClassDeclaration):
                for i in range(len(self.lines)):
                    ln = len(self.lines) - i - 1
                    if self.lines[ln] == "":
                        continue
                    return ln


    def FindMethodRange(self):
        annotations = {}
        for path, node in self.tree.filter(javalang.tree.Annotation):
            annotations[node.position.line] = ""

        methods = {}
        last_end_index = 0
        last_method = ""
        for path, node in self.tree.filter(javalang.tree.MethodDeclaration):
            # ParseCodeBlocks(source_code, node)
            if node.name not in methods:
                entry = node.name + "_" + str(node.position.line)
                methods[entry] = {}
                methods[entry]["start"] = node.position.line

                curr = node.position.line - 1
                methods[entry]["annotation_end"] = curr
                while(1):
                    if curr in annotations:
                        curr -= 1
                    else:
                        break
                methods[entry]["annotation_start"] = curr + 1

                if last_method != "":
                    methods[last_method]["end"] = []
                    for e in range(len(self.return_lines)):
                        if e >= last_end_index and self.return_lines[e] < methods[entry]["start"]:
                            methods[last_method]["end"].append(self.return_lines[e])
                            last_end_index += 1
                # if last_method != "":
                #     for i in range(curr + 1):
                #         ln = curr - i
                #         if self.lines[ln] == "":
                #             continue
                #         methods[last_method]["end"] = ln - 1
                #         break
            
                last_method = entry
            
            else:
                print("[Error] Repeated method name", self.fname, node.name)
            
            # methods[last_method]["end"] = self.end_line

            methods[last_method]["end"] = []
            for e in range(last_end_index, len(self.return_lines)):
               methods[last_method]["end"].append(self.return_lines[e])

        return methods


    def ParseCodeBlocks(self):
        fine_blocks = []
        coarse_blocks = []
        for path, node in self.tree.filter(javalang.tree.MethodDeclaration):
            method = node.body
            if method == None or len(method) == 0:
                return None, None
            ends = self.methods[node.name + "_" + str(node.position.line)]["end"]
            for end in ends:
                coarse_blocks.append((method[0].position.line, end))

            start = 0
            end = 0
            for i in range(len(method)):
                start = method[i].position.line

                if i < len(method) - 1:
                    end = method[i+1].position.line
                    for temp_end in ends:
                        if temp_end > start and temp_end < end:
                            end = temp_end
                            fine_blocks.append((start, end))
                    
                    fine_blocks.append((start, method[i+1].position.line))
                else:
                    for end in ends:
                        if end >= start:
                            fine_blocks.append((start, end))

        return fine_blocks, coarse_blocks



if __name__ == '__main__':
    train_ticket_path = "/users/lzhang/train-ticket/"

    coarse_blocks_file = "coarse_block.lms"
    fine_blocks_file = "fine_blocks.lms"
    coarse_blocks_out = open(coarse_blocks_file, "w")
    fine_blocks_out = open(fine_blocks_file, "w")

    for root, dirs, files in os.walk(train_ticket_path):
        for file in files:
            fname = os.path.join(root, file)
            if ".java" in fname and "Test.java" not in fname and "old-doc" not in fname:
                # if "train-ticket/ts-travel-service/src/main/java/travel/service/TravelServiceImpl.java" not in fname:
                #     continue
                with open(fname, "r") as f:
                    source_code = f.read()
                    parser = Parse(fname, source_code)
                    if parser.isValid:
                        if parser.coarse_blocks != None:
                            if len(parser.coarse_blocks):
                                coarse_blocks_out.write(fname+"\n")
                                for item in parser.coarse_blocks:
                                    if item[0] > item[1]:
                                        print("Error")
                                    coarse_blocks_out.write(str(item)+"\n")
                        
                        if parser.fine_blocks != None:
                            if len(parser.fine_blocks):
                                fine_blocks_out.write(fname+"\n")
                                for item in parser.fine_blocks:
                                    if item[0] > item[1]:
                                        print("Error")
                                    fine_blocks_out.write(str(item)+"\n")

    coarse_blocks_out.close()
    fine_blocks_out.close()