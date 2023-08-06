from ..models.modelloader import ModelLoader
from ..dataloader.loader import DataLoader
import torch
from ..training.train_params import train_helper
import tqdm
from torch.utils.tensorboard import SummaryWriter
import os
from mb_utils.src.logging import logger
import numpy as np
from ..utils.viewer import gradcam_viewer,create_img_grid,plot_classes_pred

__all__ = ['classification_train_loop']

def classification_train_loop( k_data,data_model,model,train_loader,val_loader,loss_attr,optimizer,scheduler=None,writer=None,logger=None,gradcam=None,gradcam_rgb=False,device='cpu'):
    """
    Function to train the model
    Args:
        data: data dictionary YAML of DataLoader
        data_model: model parameters - data.data_dict['model']
        model: model to be trained
        train_loader: train dataloader
        val_loader: validation dataloader
        loss_attr: loss function
        optimizer: optimizer
        scheduler: scheduler
        writer: tensorboard writer
        logger: logger
        gradcam: gradcam layers to be visulized
        device: default is cpu
    output:
        None
    """

    model.to(device)

    for i in tqdm.tqdm(range(data_model['model_epochs'])):
        
        ##train loop
        
        model.train(True)
        print('model train true')
        train_loss = 0
        
        if logger:
            logger.info('Training Started')
        for j,(x,y) in enumerate(train_loader):
            x,y = x.to(device),y.to(device)
            optimizer.zero_grad()
            y_pred = model(x)
            current_loss = loss_attr(y_pred,y)
            current_loss.backward()            
            optimizer.step()
            if scheduler is not None:
                scheduler.step()    
            train_loss += current_loss.item()
            if logger:
                logger.info(f'Epoch {i+1} - Batch {j+1} - Train Loss: {current_loss.item()}')
            
            
            #get grad cam images
            if gradcam and writer is not None:
                x_grad = x[0,:].to('cpu')
                x_grad = x_grad.unsqueeze(0)
                #y_grad = y[0].to('cpu')
                use_cuda=False
                if device.type != 'cpu':
                    use_cuda = True
                for cam_layers in gradcam:
                    grad_img = gradcam_viewer(cam_layers,model,x_grad,gradcam_rgb=gradcam_rgb,use_cuda=use_cuda)
                    if grad_img is not None:
                        grad_img = np.transpose(grad_img,(2,0,1))
                        writer.add_image(f'Gradcam/{cam_layers}',grad_img,global_step=i)
                    if j == 0:
                        if grad_img is None:
                            if logger:
                                logger.info(f'Gradcam not supported for {cam_layers}')
            if writer is not None and j==1:
                create_img_grid(x,y,writer,global_step=i)

        avg_train_loss = train_loss / len(train_loader)
        if logger:
            logger.info(f'Epoch {i+1} - Train Loss: {avg_train_loss}')
    
        if writer is not None:
            writer.add_graph(model, x)
            writer.add_scalar('Loss/train', avg_train_loss, global_step=i)
            for name, param in model.named_parameters():
                writer.add_histogram(name, param, global_step=i)
            
        #validation loop

        val_loss = 0
        val_acc = 0
        new_val_loss = 0
        #num_samples = 0
    
        print('lr = ',optimizer.param_groups[0]['lr'])
        print('momentum = ',optimizer.param_groups[0]['momentum'])
        print('scheduler = ',scheduler.get_lr())
        model.train(False)
        print('model train false')
        with torch.no_grad():
            for x_val, y_val in val_loader:
                x_val, y_val = x_val.to(device), y_val.to(device)
                output = model(x_val)
                val_loss += loss_attr(output, y_val).item() * x_val.size(0)
                _, preds = torch.max(output, 1) #no need of softmax. max returns the index of the max value
                val_acc += torch.sum(preds == y_val.data)
                new_val_loss = val_loss/x_val.size(0)
                #num_samples += x_val.size(0)
                if logger: 
                    logger.info(f'Epoch {i+1} - Batch {j+1} - Val Loss: {new_val_loss:.3f}')
            
            avg_val_loss = val_loss / len(val_loader.dataset)
            val_acc = val_acc/len(val_loader.dataset)
            #val_loss /= num_samples
            #val_acc = val_acc / num_samples
            if logger:
                logger.info(f'Epoch {i+1} -Avg Val Loss: {avg_val_loss:.3f}')
                logger.info(f'Epoch {i+1} - Val Accuracy: {val_acc:.3f}')

        print(preds)
        print(y_val.data)

    
        if writer is not None:
            writer.add_scalar('Loss/val', val_loss, global_step=i)
            writer.add_scalar('Accuracy/val', val_acc, global_step=i)    
            
            #get classes/labels in a dict for the last batch
            if len(x_val)<4:
                logger.info('Batch size of last batch is less than 4. Cannot plot classes')
            else:
                prob_val = torch.nn.functional.softmax(output, dim=1)
                fig1 = plot_classes_pred(x_val, y_val, prob_val, preds)
                writer.add_figure('predictions vs. actuals', fig1, global_step=i)
    
        # save best model
        if i == 0:
            best_val_loss = float('inf')
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_model = model.state_dict()

            path = os.path.join(k_data['work_dir'], 'best_model.pth')
            torch.save(best_model, path)
            if logger:
                logger.info(f'Epoch {i+1} - Best Model Saved')
        


        
        
