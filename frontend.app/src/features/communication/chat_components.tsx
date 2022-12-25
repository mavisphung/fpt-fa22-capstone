import {
    ComponentPropsWithoutRef,
    ElementType,
    ReactNode
} from 'react'

type MyDivProps<T extends ElementType> = {
    as?: T,
    children: ReactNode;
}

export const MyDiv = <T extends ElementType = "div">(
    {
        as, children,...props
    }: MyDivProps<T> & ComponentPropsWithoutRef<T>
)=>{
    const Component = as || 'div';
    return <Component {...props}>{children}</Component>
} 
