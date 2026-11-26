# Analysis

## Layer 7, Head 10

This attention head appears to focus on the relationship between verbs and their objects.

In the first example, the word `[MASK]` gives strong attention to the word "chased". This suggests that the model is identifying the relationship between the verb and the missing word that receives the action.

In the second example, the word "Bob" gives strong attention to the word "gave". This also shows a relationship between a verb and the person receiving its action.

**Example sentences:**

1. The dog chased the [MASK] because it was excited.
2. Alice gave Bob her [MASK] because she trusted him.

## Layer 4, Head 4

This attention head appears to focus on relationships between pronouns and the predicates associated with them.

In the first example, the pronoun "it" gives strong attention to the word "excited". In the second example, the pronoun "she" gives strong attention to the word "trusted".

This suggests that the attention head may help connect pronouns with the actions or descriptions associated with them.

**Example sentences:**

1. The dog chased the [MASK] because it was excited.
2. Alice gave Bob her [MASK] because she trusted him.

## Conclusion

The attention diagrams show that different attention heads focus on different relationships between words. Some heads appear to connect verbs with their objects, while others focus on relationships between pronouns and their associated predicates. These patterns help demonstrate how BERT uses attention to understand relationships within sentences.