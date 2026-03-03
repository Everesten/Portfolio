import matplotlib.pyplot as plt

def create_amino_histogram(plot_name, aminos):

    plt.hist(list(aminos))
    plt.title("Histogram of Amino Acids")
    plt.xlabel('Amino Acid Abbreviations')
    plt.ylabel('Counts')
    plt.savefig(plot_name)

def create_GC_scatter(plot_name, gc_ratios, sequence_lengths):

    plt.scatter(gc_ratios, sequence_lengths)
    plt.title("Scatterplot of Sequence Length vs GC Content")
    plt.xlabel('GC Content Ratio')
    plt.ylabel('Sequence Length')
    plt.savefig(plot_name)

def create_base_lineplot(plot_name, sequence):

    y_plot = [[],[],[],[]] # T A C G
    occurance = [0, 0, 0, 0] # T A C G
    sequence = list(sequence)

    for i, letter in enumerate(sequence):
        
        i += 1

        if letter == "T":
            occurance[0] += 1
        elif letter == "A":
            occurance[1] += 1
        elif letter == "C":
            occurance[2] += 1
        else:  
            occurance[3] += 1

        y_plot[0].append(occurance[0]/i)
        y_plot[1].append(occurance[1]/i)
        y_plot[2].append(occurance[2]/i)
        y_plot[3].append(occurance[3]/i)
        
    x_plot = range(1, len(sequence) + 1)

    plt.title("Line Plot of Base Ratios")
    plt.xlabel('Location in Sequence')
    plt.ylabel('Ratio Per Base')


    plt.plot(x_plot, y_plot[1], label="A")
    plt.plot(x_plot, y_plot[0], label="T")
    plt.plot(x_plot, y_plot[3], label="G")
    plt.plot(x_plot, y_plot[2], label="C")
    plt.legend(loc='best')

    plt.savefig(plot_name)

def dna_to_rna(sequence):
    rna = ""
    for letter in sequence:
        if letter == "A":
            rna += "U"
        if letter == "T":
            rna += "A"
        if letter == "G":
            rna += "C"
        if letter == "C":
            rna += "G"
    return rna

def GC_Ratios(sequence):
    
    GC_count = 0.0
    
    for letter in sequence:
        if letter == "G" or letter == "C":
            GC_count += 1.0
    
    return GC_count/len(sequence)

def parse_file_into_acids(filename):

    with open(filename, "r") as file:
        parsed = []
        lines = file.readlines()
        for sequence in lines:
            items = sequence.split()
            parsed.append(items)
        
    return parsed

def find_sequence(sequence):
    
    raw_rna_seq = dna_to_rna(sequence)
    rna_seq = []

    if "AUG" in raw_rna_seq:
        begin = raw_rna_seq.index("AUG") + 3
        cursor = begin
        while cursor < len(raw_rna_seq):
            
            chunk = raw_rna_seq[cursor:cursor+3]

            if "UAA" in chunk:
                break
            elif "UGA" in chunk:
                break
            elif "UAG" in chunk:
                break

            rna_seq.append(chunk)

            cursor += 3

    return rna_seq

def connect_seq(template, sequence):
    
    rna_seq = find_sequence(sequence)

    acid_seq = 'M'

    for chunk in rna_seq:
        for acid in template:
            if chunk == acid[0]:
                acid_seq += acid[2]
                break
    
    return acid_seq

def flatten(xss):
    return [x for xs in xss for x in xs]

if __name__ == "__main__":
    
    codon_file = "codons.dat"
    sequence_file = "sequences.dat"
    plot_to_produce = 3
    output_file = "plot.png"

    # codon_file = input()
    # sequence_file = input()
    # plot_to_produce = int(input())
    # output_file = input()

    template = parse_file_into_acids(codon_file)

    with open(sequence_file, "r") as seqfile:
        
        aminos = []
        GC_Ratio = []
        seq_lengths = []
        sequences = []

        for line in seqfile.readlines(): 
            
            if "DONE" in line:
                break

            line = line.strip()

            aminos.append(list(connect_seq(template, line))) 
            GC_Ratio.append(GC_Ratios(line)) 
            seq_lengths.append(len(line))
            sequences.append(line)
        
        aminos = flatten(aminos)

        if plot_to_produce == 1:
            # Requires plot_name, aminos
            create_amino_histogram(output_file, aminos)
        elif plot_to_produce == 2:
            # Requires plot_name, gc_ratios, sequence_lengths
            create_GC_scatter(output_file, GC_Ratio, seq_lengths)
        else:
            sequence_num = int(input())
            # Requires plot_name, sequence
            create_base_lineplot(output_file, sequences[sequence_num])

