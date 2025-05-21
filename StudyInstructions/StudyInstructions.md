# Welcome! #

Thank you for participating in APCL lab's research study. Your participation in this study is voluntary and may end any time you choose. 

The overall aim of this study is to record programmer eye-movements during the completion of a code identification and localization task. 

### Overall Task ###
For the task, we will present you with a bug report. 
After reading the bug report, you will look at the code and attempt to identify what the cause of the bug is and where the cause of the bug is. 
Then, you will explain what you have found in your answer. 


Here is an example: 
## Bug Report: ##

----------------------------------------------------------------------------------------------------------------------------------------------
There is a memory leak in my program `test_mem.c`, but I don’t know where. 
When I run my program with valgrind, this is the output. 

```
==3211329== Memcheck, a memory error detector
==3211329== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==3211329== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==3211329== Command: ./test_mem
==3211329==
Enter number of elements:10
Entered number of elements: 10
Memory successfully allocated using malloc.
The elements of the array are: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
==3211329==
==3211329== HEAP SUMMARY:
==3211329==     in use at exit: 40 bytes in 1 blocks
==3211329==   total heap usage: 3 allocs, 2 frees, 2,088 bytes allocated
==3211329==
==3211329== 40 bytes in 1 blocks are definitely lost in loss record 1 of 1
==3211329==    at 0x4C37135: malloc (vg_replace_malloc.c:381)
==3211329==    by 0x400727: main (in /escnfs/home/esmith36/research/test_mem)
==3211329==
==3211329== LEAK SUMMARY:
==3211329==    definitely lost: 40 bytes in 1 blocks
==3211329==    indirectly lost: 0 bytes in 0 blocks
==3211329==      possibly lost: 0 bytes in 0 blocks
==3211329==    still reachable: 0 bytes in 0 blocks
==3211329==         suppressed: 0 bytes in 0 blocks
==3211329==
==3211329== For lists of detected and suppressed errors, rerun with: -s
==3211329== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

## Code: 

```
1 #include <stdio.h>
2 #include <stdlib.h>
3 
4 int main()
5 {
6
7    int* ptr;
8    int n, i;
9
10    printf("Enter number of elements:");
11    scanf("%d",&n);
12    printf("Entered number of elements: %d\n", n);
13
14    ptr = (int*)malloc(n * sizeof(int));
15
16    if (ptr == NULL) {
17        printf("Memory not allocated.\n");
18        exit(0);
19    }
20    else {
21
22        printf("Memory successfully allocated using malloc.\n");
23
24        for (i = 0; i < n; ++i) {
25            ptr[i] = i + 1;
26        }
27
28        printf("The elements of the array are: ");
29        for (i = 0; i < n; ++i) {
30            if (i == (n-1)) {
31                printf("%d\n", ptr[i]);
32            } else {
33                printf("%d, ", ptr[i]);
34            }
35        }
36    }
37
38    return 0;
39 }
```
------------------------------------------------------------------------------------------------------------------------------------------------------------
## Expected Answer: ## 

Question 1: What is the cause of the bug?  
Answer: The memory leak is due to the fact that `test_mem.c` does not `free` the memory allocated on line 14 called `ptr`. 

Question 2: At which line number(s) does the bug occur? Please try to localize to as fine of a granularity as you can.   
Answer: The bug occurs when the program returns on line 38. At that point, we no longer have access to the allocated memory `ptr`. 
The program is done using `ptr` after the close of the if statement on line 36, but before the return statement on line 38. 
At that point, it should be freed. One place to free would be on line 37.

-------------------------------------------------------------------------------------------------------------------------------
## Logistics 

### Pop-Ups 
Periodically throughout the study, a pop-up window will appear on your screen.   
Please answer the question promptly and submit your responses.   
These pop-ups will appear every 5 minutes.   
They will ask you the following question:   
In the few seconds before this screen appeared, what were you thinking about?  
The answer choices are:   
- I was focused on the task.
- I was thinking about my performance on the task or how long it is taking.
- I was thinking about things unrelated to the task (e.g., daydreaming)
- I was distracted by sights or sounds in my environment.
- My mind was blank.


### Timing 
There are 6 bugs available to you, but you do not need to attempt all 6 bugs. 
Start the first bug, and work on it for at least 10 minutes but no more than 30 minutes. 
Repeat this until the study has lasted a total of 120 minutes (including setup). 
The study administrator will help keep track of time. 
Between 10 and 30 minutes you may decide that you are not making progress on a bug and 
choose to move on to the next bug. You may not go back to a previous bug once you have moved on. 

### Markdown Preview  
For some of the bug reports, you may wish to open them with the Markdown 
Previewer. To do this: 
on the top bar select `Window -> Show View ->  Other -> 
search for "Preview" and select the Preview option` 


-------------------------------------------------------------------------------------------------------------------------------
## More Information on Completing the Tasks

### Projects 
Different bugs/tasks may be in the same project. For example, bugs 1 and 3 might both be bugs in openssl. 
However, the versions of the code for bugs 1 and 3 may be different. 

### Finding Bugs 
Not all the information required to come up with the answer will be included in 1 file. 
We expect you to investigate as many files as necessary to discover where the bug is. 
You may use the Eclipse IDE features like call-graph to aid in this effort. 
However, you are not allowed to run the program. 
The only output you can refer to is the output in the bug report. 


### Outside Resources 
We are providing the Remain AI plugin for Eclipse. This AI is ChatGPT 4o, and you may ask it questions 
when you feel that you need help. However, please do not copy and paste code, and please do not
ask questions or provide information that would indicate to the AI that you are working on 
a specific open source project like redis or openssl. You may ask the AI general questions 
about syntax, man pages, etc.   

*Please do not clear the Ai Chat Window at any point during the study.*   

-------------------------------------------------------------------------------------------------------------------------- 
## Answering ##

### What is the cause of the bug? ### 
When answering this question, please give as detailed of an answer as possible. 
If possible, please refer to line numbers. 
In many cases, the bug report will answer this question to some extent. 
Please feel free to use information from the bug report to answer this as well as your own thoughts. 
When answering this question think about questions like "What caused the memory leak?", "What caused the buffer overflow?", etc. 

### At which line number(s) does the bug occur? ### 
When answering this question, please give as detailed of an answer as possible 
(See the following section about Incomplete Answers). 
When answering this question, think about questions like "Which line of code is the second free (in double free bugs)?", 
"Which line of code attempts to access invalid memory?", etc. 

### Missing Code and Memory Leaks ###
In some cases like the example above, the bug occurs because a line(s) of code is missing. 
If this is the case, you will need to explain where the bug occurs and/or where to insert the missing line(s) of code with as much detail as possible. 
For memory leaks, we define where the bug occurs the same way that tools like valgrind do. 
For memory leaks, the bug occurs the moment we lose access to allocated memory. 

### Incomplete Answers ###
Please provide as much detail as possible. 
Even if you do not know exactly which line number is the cause of the bug, please tell us what you do know or what your guess is. 
Try to localize as much as possible to a file, function, block of code, or set of line numbers. 
For example, you might have a guess as to which file the bug is in, but you do not know where in the file the bug is. 
In this case, please tell us what file you believe the bug is in. 
If you have an educated guess about what the bug is or where it is, please write down your guess. 
You do not need to be 100% sure of your answers.

### Bug Fixes ###
You are not required to figure out *how to fix* the bug or to explain a bug fix. Focus on identify *what* and *where*.  
 
 -----------------------------------------------------------------------------------------------------------------------
 
# Please confirm to your study administrator that you understand the task and ask them any questions you might have before proceeding.

Done? Lets Begin!

# Open the file `StudyProcedure.md`


