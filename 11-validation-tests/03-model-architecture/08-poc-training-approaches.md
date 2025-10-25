# Test 08: POC Training Approaches

## Objective
Test and compare three different approaches to training semantic compression models

## Three POC Approaches to Test

### Option 1: Few-Shot Prompting (No Training Required)
**Timeline**: 1-2 days setup, immediate testing
**Data Needed**: 5-10 example video→JSON pairs as prompts
**Models to Test**: GPT-4, Claude 3.5 Sonnet, Gemini Pro
**Test Set**: 20-30 new videos for validation

### Option 2: Minimal Fine-Tuning (SKIP - Too Expensive for Solo)
**Why Skip**: Requires 50-100 annotations (weeks of work) + cloud GPU costs

### Option 3: LoRA Fine-Tuning (REALISTIC)
**Timeline**: 1 day setup + 4 hours training
**Data Needed**: 5 examples (your test videos + manual JSON)
**Target Models**: Mistral-7B with LoRA (fits on 5090)
**Training Time**: 2-4 hours on your RTX 5090
**Cost**: Free (local training)

## Detailed Execution Process

### Phase 1: Few-Shot Prompting Setup (Days 1-2)

#### Step 1: Create Example Pairs (Use Your 5 Test Videos)
1. **Use Your Test Videos from Day 1**
   - Take the 5 videos you already tested
   - Use the best GPT-4 Vision outputs as starting points
   - Manually clean up 2-3 JSON examples to be "perfect"

2. **Design Few-Shot Prompt Template**```
You 
are an expert at converting video content into structured semantic JSON representations. Here are examples of high-quality conversions:

EXAMPLE 1:
Video Description: [Detailed scene description]
JSON Output: [Perfect JSON structure]

EXAMPLE 2:
Video Description: [Another scene description]
JSON Output: [Another perfect JSON structure]

[Continue for 3-5 examples]

Now convert this new video:
Video Description: [New video to convert]
JSON Output:
```

#### Step 2: Test Execution Process
1. **GPT-4 Testing**
   - Run 20 test videos through few-shot prompt
   - Measure JSON quality and consistency
   - Document failure modes

2. **Claude 3.5 Testing**
   - Same test set with Claude-optimized prompts
   - Compare performance with GPT-4
   - Analyze different reasoning approaches

3. **Gemini Pro Testing**
   - Test multimodal capabilities
   - Compare with text-only approaches
   - Evaluate cost-effectiveness

### Phase 2: Minimal Fine-Tuning (Weeks 1-2)

#### Step 1: Dataset Preparation
1. **Collect 50-100 Video Clips**
   - Diverse genres and lengths
   - Clear usage rights
   - High-quality source material

2. **Manual JSON Annotation Process**
   ```
   ANNOTATION GUIDELINES:
   1. Watch video completely first
   2. Identify key semantic elements
   3. Create JSON following established schema
   4. Review for consistency and completeness
   5. Validate JSON syntax
   6. Cross-check with second annotator
   ```

3. **Quality Control Process**
   - Inter-annotator agreement >85%
   - JSON schema validation
   - Semantic completeness review

#### Step 2: Model Selection and Setup
1. **T5-Base Fine-Tuning**
   ```python
   from transformers import T5ForConditionalGeneration, T5Tokenizer
   from transformers import Trainer, TrainingArguments
   
   # Model setup
   model = T5ForConditionalGeneration.from_pretrained('t5-base')
   tokenizer = T5Tokenizer.from_pretrained('t5-base')
   
   # Training configuration
   training_args = TrainingArguments(
       output_dir='./semantic-compression-t5',
       num_train_epochs=3,
       per_device_train_batch_size=4,
       per_device_eval_batch_size=4,
       warmup_steps=500,
       weight_decay=0.01,
       logging_dir='./logs',
   )
   ```

2. **Data Preprocessing**
   ```python
   def preprocess_data(video_description, json_output):
       input_text = f"Convert to semantic JSON: {video_description}"
       target_text = json_output
       
       input_ids = tokenizer.encode(input_text, return_tensors='pt')
       target_ids = tokenizer.encode(target_text, return_tensors='pt')
       
       return {
           'input_ids': input_ids,
           'labels': target_ids
       }
   ```

#### Step 3: Training Process
1. **Training Execution**
   - 3-5 epochs on prepared dataset
   - Monitor validation loss
   - Save checkpoints regularly

2. **Evaluation During Training**
   - JSON syntax validation rate
   - Semantic completeness scores
   - Comparison with few-shot baseline

### Phase 3: LoRA Fine-Tuning (Days 1-5)

#### Step 1: LoRA Setup
1. **Model Selection**
   ```python
   from peft import LoraConfig, get_peft_model, TaskType
   from transformers import LlamaForCausalLM, LlamaTokenizer
   
   # Base model setup
   model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
   tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
   
   # LoRA configuration
   lora_config = LoraConfig(
       task_type=TaskType.CAUSAL_LM,
       inference_mode=False,
       r=8,
       lora_alpha=32,
       lora_dropout=0.1,
       target_modules=["q_proj", "v_proj"]
   )
   
   model = get_peft_model(model, lora_config)
   ```

2. **Efficient Data Preparation**
   - Use 20-50 highest quality examples
   - Focus on diverse, representative cases
   - Optimize for LoRA training efficiency

#### Step 2: Training Process
1. **LoRA Training Script**
   ```python
   from transformers import TrainingArguments, Trainer
   
   training_args = TrainingArguments(
       output_dir="./lora-semantic-compression",
       per_device_train_batch_size=1,
       gradient_accumulation_steps=4,
       num_train_epochs=3,
       learning_rate=2e-4,
       fp16=True,
       save_steps=50,
       logging_steps=10,
   )
   
   trainer = Trainer(
       model=model,
       args=training_args,
       train_dataset=train_dataset,
       eval_dataset=eval_dataset,
   )
   
   trainer.train()
   ```

2. **Monitoring and Optimization**
   - Track training loss and convergence
   - Monitor GPU memory usage
   - Validate output quality during training

## Comparative Analysis Framework

### Success Metrics for All Approaches:
- **JSON Format Compliance**: >95%
- **Semantic Completeness**: >75%
- **Human Evaluator Agreement**: >80%
- **Processing Time**: <5 minutes per video clip
- **Cost per Video Processed**: <$1.00

### Evaluation Process:

#### Week 3: Comprehensive Comparison
1. **Quality Assessment**
   ```
   EVALUATION CRITERIA:
   1. JSON Schema Compliance (0-100%)
   2. Semantic Accuracy (0-100%)
   3. Consistency Across Runs (0-100%)
   4. Cultural Sensitivity (0-100%)
   5. Processing Speed (seconds)
   6. Cost per Video ($)
   ```

2. **Statistical Analysis**
   - ANOVA testing for significant differences
   - Confidence intervals for performance metrics
   - Cost-benefit analysis for each approach

#### Detailed Comparison Template:
```
APPROACH COMPARISON MATRIX:

                    Few-Shot    Fine-Tuning    LoRA
JSON Compliance     [score]     [score]        [score]
Semantic Accuracy   [score]     [score]        [score]
Consistency         [score]     [score]        [score]
Setup Time          [hours]     [hours]        [hours]
Training Time       [hours]     [hours]        [hours]
Data Requirements   [examples]  [examples]     [examples]
Cost per Video      [$]         [$]            [$]
Scalability         [rating]    [rating]       [rating]
Customization       [rating]    [rating]       [rating]
```

## Execution Timeline

### Week 1: Few-Shot Implementation
- Days 1-2: Setup and prompt engineering
- Days 3-4: Testing across all models
- Day 5: Results analysis and documentation

### Week 2: Fine-Tuning Setup
- Days 1-3: Dataset preparation and annotation
- Days 4-5: Model training and initial evaluation

### Week 3: LoRA Implementation
- Days 1-2: LoRA setup and data preparation
- Days 3-4: Training and optimization
- Day 5: Final evaluation and comparison

### Week 4: Analysis and Reporting
- Days 1-2: Comprehensive performance analysis
- Days 3-4: Cost-benefit analysis and recommendations
- Day 5: Final report and next steps planning

## Success Criteria
- At least one approach achieves all target metrics
- Clear recommendation for production implementation
- Validated training pipeline for chosen approach
- Cost and scalability projections for commercial use

## Deliverables
1. **Performance Comparison Report**: Detailed analysis of all three approaches
2. **Recommended Implementation**: Best approach with rationale
3. **Training Pipeline Documentation**: Complete setup and execution guide
4. **Cost Analysis**: Detailed breakdown of development and operational costs
5. **Scalability Assessment**: Projections for larger-scale implementation
6. **Next Phase Recommendations**: Roadmap for production development

## Next Steps
Results inform production model development and integration with content regeneration pipeline from Test 03.