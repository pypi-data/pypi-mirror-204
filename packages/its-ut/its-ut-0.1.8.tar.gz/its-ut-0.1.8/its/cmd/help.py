
from its.cmd import (
    channel_capacity,
    fisher_information,
    huffman_code,
    kl_divergence,
    lempel_ziv,
    shannon_entropy,
    smallest_sufficient_set,
    typical_set,
)

help = """
This project is the result of a group effort for the Information Theory
& Statistics (ITS) course at the University of Twente, the Netherlands.
A few subexercises of some of the assignments included some coding
challenges. This made us thought, that it would be cool to have a small
software suite, which covers several aspects of the ITS course.

The project is a Python command-line utility. The project is available
on Python Package Index, pypi.org. The installation is described later
in this document.

The tool is a command-line utility which covers plenty of features. This
means, we implemented sub-commands for each different feature set. If
you install the tool, it will be available as the command-line tool
`its-ut`.  We demonstrate the usage with code snippets. We start by
explaining how to get help/assistance from the tool itself. First and
foremost, we implemented a help subcommand. This subcommand describes
how to use the tool:

    its-ut help

To get more information about one of the subcommands, use:

    its-ut help <command name>

Furthermore, there is always the option to use the --help flag, which
prints a short summary of how to use the tool. You can either use --help
after the main command, or after one of the subcommands:

    its-ut --help
    its-ut shannon-entropy --help

We suggest exploring all of the help texts and the short summary of
options with --help for each of the subcommands. That should give you a
clear idea, what the tool can and cannot do.

Furthermore, this tool is a generalization for certain problem
statements taught in this course. Unlike a human mind, which can solve
any arbitrary problem with just enough effort, we had to somehow model
all of these problem statements onto something that can be solved
automatically. This led to the design decision that we use discrete and
finite probabilities only. Most of the subcommands require a
distribution as the basis for the calculations performed. For instance,
to calculate the Shannon Entropy, you have to define for which
distribution you want to calculate the Shannon Entropy.

Therefore, we defined a text-based file-format which models these finite
and discrete distributions. Each distribution is defined with a symbol,
and the corresponding probability. The format is as follows:

    <symbol: string>, <expression: string>

The symbol is any arbitrary symbol you want to define for the
probability. The expression is a mathematical expression that will be
evaluated to a floating point number. It becomes clear with an example.
To define the Bernoulli distribution with p=0.4 you can define the
distribution file as follows.

Note: Lines that begin with a # are comments and will not be parsed.

    ```bernoulli.csv
    # Bernoulli Distribution
    # p
    p, 4 / 10
    # 1 - p
    q, 6 / 10
    ```

In this case, we use p and q as the labels/symbols for the corresponding
probabilities. Just store this distribution in a text file called
`bernoulli.csv`. To use this file in the subcommands, just use the
corresponding subcommand and check out the command-line arguments it
requires.


Walkthrough
===========

This section should provide a walkthrough on how to solve a certain
problem with this tool. We defined our Bernoulli distribution above:

    p=0.4
    q=0.6

For the Kullback-Leibner Divergence we need to define another
distribution to compare to. Thus, we define another distribution - in
this case the uniform Bernoulli distribution:

    ```bernoulli-uniform.csv
    # Uniform Bernoulli with p=0.5
    p, 1/2
    q, 1/2
    ```
We store this file in bernoulli-uniform.csv. Now, we need to understand
how to use the tool. We start with the help command its-ut help. This
prints us an on-screen guide on how to use the tool:

    its-ut help

The output on the screen reveals that we have a module/subcommand called
`kl-divergence`. Therefore, we print the help of the kl-divergence
submodule too:

    its-ut help kl-divergence


We get a proper description of the KL divergence module. Furthermore, we
want to know the command line options. We use the --help flag:

    its-ut kl-divergence --help

We see, it requires a probability -p and a probability -q. We have all
the information we need for the full command. We remember, we stored our
input distibutions under bernoulli.csv and bernoulli-uniform.csv. We
also know that the KL divergence is a non-symmetric distance measure.
Thus, we calculate it with p being first P~B(0.4) and then with P~B(0.5).

    its-ut kl-divergence -p bernoulli.csv -q bernoulli-uniform.csv

    $>0.020135513551

    its-ut kl-divergence -p bernoulli-uniform.csv -q bernoulli.csv

    $> 0.020410997260

This was a full walkthrough on how to use the tool.


Limitations
===========

To stick within the boundaries of the project, we had to limit ourselves
to certain limitations. The course itself included theory about discrete
as well as continuous probability density functions. With this project,
we wanted to generalize problem statements. This however revealed to be
a significant challenge that is not too easy to overcome. As an example,
the Fisher information requires to find the first and second derivative
of a PDF. We restrained ourselves from implementing a complete Calculus
framework and tried to focus on the ITS aspects. This means, we limit
our input to discrete and finite probability functions. The software has
a bunch of modules. We use the term command and module as synonyms in
the help texts. Each command has its own set of options and arguments. 

Furthermore, for time constraints, we do not use decimal types with
arbitrary precisions. Instead, we use the regular 64-bit floating point
numbers. This means that the calculations are slightly off from the real
calculations, simply because floating point numbers are base 2
approximations from the decimal numbers. Generally speaking, the
approximations are good enough to confirm hand-written calculations.


Modules
=======

This is a list of all the modules implemented in this tool:

    * channel-capacity
    * fisher-information
    * huffman-code
    * kl-divergence
    * lempel-ziv
    * shannon-entropy
    * smallest-sufficient-set
    * typical-set

Use help with one of those descriptors to get a detailled help how that
module is designed, which assumptions were made and how to use it.

"""

def fn(args):
    if args.module is None:
        print(help)
    elif args.module == "channel-capacity":
        print(channel_capacity.__doc__)
    elif args.module == "fisher-information":
        print(fisher_information.__doc__)
    elif args.module == "huffman-code":
        print(huffman_code.__doc__)
    elif args.module == "kl-divergence":
        print(kl_divergence.__doc__)
    elif args.module == "lempel-ziv":
        print(lempel_ziv.__doc__)
    elif args.module == "shannon-entropy":
        print(shannon_entropy.__doc__)
    elif args.module == "smallest-sufficient-set":
        print(smallest_sufficient_set.__doc__)
    elif args.module == "typical-set":
        print(typical_set.__doc__)
    else:
        print(f"'{args.module}' is not a valid module. Either leave it empty, or use any of the defined commands.")
    
