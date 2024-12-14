import gradio as gr
import random

# Функция для обработки изображений
def process_images(images):
    results = []

    for image in images:
        label = f"Класс: {random.randint(1, 10)}"
        results.append((image, label))
    
    if not results:
        results.append(("https://placehold.jp/e6e6e6/4d2cdd/200x200.png?text=There%20is%20nothing%20to%20evaluate",''))
    return results

def prepare_images():
    # Список изображений по умолчанию
    default_images = ["https://placebear.com/300/300.jpg",
                      "https://placebear.com/400/400.jpg",
                      "https://placebear.com/500/500.jpg",
                      ]
    return default_images

# Интерфейс
with gr.Blocks() as demo:
    gr.Markdown("### Демонстрации работы модели")
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Files(file_types=["image"], 
                                   type="filepath",
                                   label="Выберите изображения",)
            with gr.Row():
                with gr.Column():
                    select_default_button = gr.Button("Выбрать предзагруженные фото")
                with gr.Column():
                    process_button = gr.Button("Запустить обработку")
        with gr.Column():
            output_gallery = gr.Gallery(label="Результаты", 
                                        elem_id="output_gallery", 
                                        rows=3, 
                                        columns=2)
    
    # Обработка изображений
    def handle_images(uploaded_images):
        images = []
        if uploaded_images:
            images = uploaded_images
        return process_images(images)
    
    # Привязываем кнопки и обработчики
    process_button.click(handle_images, inputs=[image_input], outputs=output_gallery)
    select_default_button.click(prepare_images, inputs=None, outputs=[image_input])


# Запуск интерфейса
if __name__ == "__main__":
    demo.launch(share=True)
